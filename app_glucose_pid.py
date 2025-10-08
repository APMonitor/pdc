#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Streamlit app: Type-I Diabetic Blood Glucose Control
- Manual & PID (Type-B, velocity form) control of insulin infusion
- Uses scipy.integrate.odeint (NOT Euler) for plant integration
- Based on course templates for PID apps (CSTR, Two-Tank), adapted to diabetes

Run with:
    streamlit run app_glucose_pid.py
"""

import streamlit as st
import numpy as np
import pandas as pd
import time
from typing import Tuple
from scipy.integrate import odeint

# -----------------------------------------------------------------------------
# Page config
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Diabetic Glucose PID Control", layout="wide")
st.title("Artificial Pancreas")
st.caption("Regulate blood glucose for a Type-I diabetic by manipulating insulin infusion.")

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
def ensure_default(name, val):
    if name not in st.session_state:
        st.session_state[name] = val

def init_state():
    # Flags & timing
    ensure_default("collecting", False)
    ensure_default("started_once", False)
    ensure_default("t0_wall", None)
    ensure_default("tick_count", 0)  # total simulation ticks completed

    # ----- Plant states (Bergman-style minimal model with gut compartments) -----
    # y = [g, x, i, q1, q2, g_gut]
    ensure_default("y", np.array([76.22, 33.33, 33.33, 16.67, 16.67, 150.0], dtype=float))

    # ----- Controller internals (Type-B / velocity form) -----
    ensure_default("u_prev", 3.0)      # previous insulin rate (mU/min)
    ensure_default("e_prev", None)     # e[k-1]
    ensure_default("pv_prev", None)    # g[k-1]
    ensure_default("pv_prev2", None)   # g[k-2]

    # Logs
    ensure_default("t_log", [])
    ensure_default("g_log", [])
    ensure_default("sp_log", [])
    ensure_default("u_log", [])
    ensure_default("mode_log", [])
    ensure_default("d_log", [])

    # UI seeds
    ensure_default("mode", "Automatic (PID)")
    ensure_default("g_sp", 80.0)      # mg/dL

    ensure_default("Kc", 0.02)        # proportional gain (Δu per mg/dL of error)
    ensure_default("Ki", 0.001)       # 1/min
    ensure_default("Kd", 0.0)         # min

    ensure_default("u_manual", 3.0)   # mU/min
    ensure_default("u_lo", 0.0)       # actuator bounds mU/min
    ensure_default("u_hi", 10.0)

    # Simulation time base
    ensure_default("Ts_sec", 300.0)   # default 5 min sample
    ensure_default("run_seconds", 24*60*60)  # maximum total ticks allowed

    # Disturbances
    ensure_default("meals_on", True)
    ensure_default("meal_scale", 1.0)  # scale multiplier for meal profile

init_state()

# -----------------------------------------------------------------------------
# Diabetes model (ODEs) – same structure/units as assignment
# -----------------------------------------------------------------------------
def diabetic_rhs(y: np.ndarray, t: float, ui: float, d: float) -> np.ndarray:
    """
    Right-hand-side for diabetic model ODEs.
    y: [g, x, i, q1, q2, g_gut]
    t: time (hr) – not used (autonomous)
    ui: insulin infusion (mU/min)
    d: meal disturbance (mmol/L-min)
    Returns dy/dt (per hour)
    """
    g, x, i, q1, q2, g_gut = y

    # Parameters (from assignment example)
    gb    = 291.0           # mg/dL
    p1    = 3.17e-2         # 1/min
    p2    = 1.23e-2         # 1/min
    si    = 2.9e-2          # 1/min * (mL/micro-U)
    ke    = 9.0e-2          # 1/min
    kabs  = 1.2e-2          # 1/min
    kemp  = 1.8e-1          # 1/min
    f     = 8.00e-1         # L
    vi    = 12.0            # L
    vg    = 12.0            # L

    dydt = np.empty(6)
    dydt[0] = -p1*(g-gb) - si*x*g + f*kabs/vg * g_gut + f/vg * d
    dydt[1] =  p2*(i-x)
    dydt[2] = -ke*i + ui
    dydt[3] = ui - kemp * q1
    dydt[4] = -kemp*(q2-q1)
    dydt[5] = kemp*q2 - kabs*g_gut

    # convert from minutes to hours for consistency with 1/min rates
    return dydt * 60.0

# -----------------------------------------------------------------------------
# Disturbance profile (meals): zero until meal, +1 hr rise, then exp decay
# -----------------------------------------------------------------------------
def meal_value_at_time(t_hr: float,
                       meal_hours=(8.0, 12.0, 18.0),
                       A_base: float = 1200.0,
                       scale: float = 1.0,
                       tau_decay_hr: float = 1.0) -> float:
    """
    Scalar meal disturbance d(t) evaluated at absolute simulation time t_hr.
    - Baseline 1000 (matches your previous builder's baseline)
    - 1 hr linear rise after meal time, then exponential decay.
    """
    val = 1000.0
    A = A_base * float(scale)
    for mh in meal_hours:
        dt = t_hr - mh
        if dt < 0.0:
            continue
        if dt < 1.0:
            val += A * (dt / 1.0)
        else:
            val += A * np.exp(-(dt - 1.0) / tau_decay_hr)
    return float(val)

# -----------------------------------------------------------------------------
# PID Type-B (velocity form, derivative on measurement), anti-windup
# -----------------------------------------------------------------------------
def pid_typeb_velocity(sp: float, pv: float, Ts_sec: float, Kc: float, Ki: float, Kd: float,
                       u_lo: float, u_hi: float) -> float:
    """
    Compute new u using Type-B PID in velocity form:
        u[k] = u[k-1] + Δu
    with
        Δu = Kc*(e[k] - e[k-1])
            + Ki*e[k]*Ts_min
            - Kd * (pv[k] - 2pv[k-1] + pv[k-2]) / Ts_min
    Anti-reset windup applied on saturation.
    """
    Ts_min = max(1e-6, Ts_sec / 60.0)  # convert to minutes

    # Initialise history on first call
    if st.session_state.e_prev is None:
        st.session_state.e_prev = sp - pv
    if st.session_state.pv_prev is None:
        st.session_state.pv_prev = pv
    if st.session_state.pv_prev2 is None:
        st.session_state.pv_prev2 = pv

    e = sp - pv
    # Direct acting controller
    s = -1.0
    # Proportional increment on the change in error
    P_inc = s * Kc * (e - st.session_state.e_prev)
    # Derivative increment: second difference of PV (derivative on measurement)
    D_inc = -s * Kd * ((pv - 2.0*st.session_state.pv_prev + st.session_state.pv_prev2) / Ts_min)
    # Candidate integral increment
    I_inc_candidate = s * Ki * e * Ts_min

    # Tentative output (unsaturated) including integral candidate
    u_prop = st.session_state.u_prev + P_inc + D_inc
    u_proposed = u_prop + I_inc_candidate

    # Anti-windup: if saturated and error drives further into saturation → drop I for this step
    if (u_proposed > u_hi and e > 0.0) or (u_proposed < u_lo and e < 0.0):
        I_inc = 0.0
        u_unsat = u_prop
    else:
        I_inc = I_inc_candidate
        u_unsat = u_proposed

    # Apply limits
    u_new = min(u_hi, max(u_lo, u_unsat))

    # Update histories
    st.session_state.e_prev = e
    st.session_state.pv_prev2 = st.session_state.pv_prev
    st.session_state.pv_prev = pv
    st.session_state.u_prev = u_new
    return u_new

# -----------------------------------------------------------------------------
# Sidebar controls
# -----------------------------------------------------------------------------
st.sidebar.title("Controls")

# Mode
st.sidebar.radio("Mode", options=["Automatic (PID)", "Manual"], key="mode")

# Setpoint
st.sidebar.slider("Glucose Setpoint (mg/dL)", 60.0, 140.0, key="g_sp", step=1.0)

# Manual vs PID tuning
if st.session_state.mode == "Manual":
    st.sidebar.slider("Manual Insulin (mU/min)",
                      float(st.session_state.u_lo), float(st.session_state.u_hi),
                      key="u_manual", step=0.1)
else:
    st.sidebar.subheader("PID (Type-B, velocity form)")
    st.sidebar.number_input("Kc (Δu per mg/dL)", min_value=0.0, step=0.01, key="Kc")
    st.sidebar.number_input("Ki (1/min)", min_value=0.0, step=0.001, format="%.3f", key="Ki")
    st.sidebar.number_input("Kd (min)", min_value=0.0, step=0.1, key="Kd")

# Actuator limits
u_lo_hi = st.sidebar.slider("Insulin Limits (mU/min)", 0.0, 15.0,
                            value=(float(st.session_state.u_lo), float(st.session_state.u_hi)))
st.session_state.u_lo, st.session_state.u_hi = map(float, u_lo_hi)
st.sidebar.caption(f"Limits applied: {st.session_state.u_lo:.1f}…{st.session_state.u_hi:.1f} mU/min")

# Timing
st.sidebar.number_input("Sample Time Ts (sec)", min_value=5.0, step=300.0, key="Ts_sec")
st.sidebar.number_input("Max Run Length (sec, total)", min_value=60, step=60, key="run_seconds")

# Disturbances
# (Left the meals toggle commented to avoid widget default/session-state conflict)
# st.sidebar.checkbox("Enable Meal Disturbances", value=bool(st.session_state.meals_on), key="meals_on")
st.sidebar.number_input("Meal Intensity Scale (×)", min_value=0.0, step=0.1, key="meal_scale")

# -----------------------------------------------------------------------------
# Buttons
# -----------------------------------------------------------------------------
colA, colB, _ = st.columns([1, 1, 2])
with colA:
    if st.button("Start"):
        st.session_state.collecting = True
        st.session_state.t0_wall = time.time()
        # reset logs
        st.session_state.t_log = []
        st.session_state.g_log = []
        st.session_state.sp_log = []
        st.session_state.u_log = []
        st.session_state.mode_log = []
        st.session_state.d_log = []
        # reset controller memories
        st.session_state.u_prev = float(st.session_state.u_manual) if st.session_state.mode == "Manual" else 3.0
        st.session_state.e_prev = None
        st.session_state.pv_prev = None
        st.session_state.pv_prev2 = None
        # reset plant to default initial state
        st.session_state.y = np.array([76.22, 33.33, 33.33, 16.67, 16.67, 150.0], dtype=float)
        # reset absolute tick counter
        st.session_state.tick_count = 0
        st.session_state.started_once = True

with colB:
    if st.button("Stop"):
        st.session_state.collecting = False

# -----------------------------------------------------------------------------
# Trend placeholders
# -----------------------------------------------------------------------------
chart_top = st.empty()   # Glucose PV, SP (mg/dL) with healthy band
chart_mid = st.empty()   # Insulin rate (mU/min)
chart_bot = st.empty()   # Disturbance (meal) series
status = st.empty()

# -----------------------------------------------------------------------------
# Simulation loop (continues across reruns via session_state.tick_count)
# -----------------------------------------------------------------------------
if st.session_state.collecting:
    Ts_sec = float(st.session_state.Ts_sec)
    Ts_hr = Ts_sec / 3600.0

    # We'll simulate a **small batch** of steps each rerun so the UI stays responsive
    # and so that parameter changes (e.g., Ki) take effect immediately.
    # Choose a modest batch size, e.g., run 20 ticks per rerun.
    batch_steps = 2000

    # Protect against exceeding total allowed run length
    max_total_steps = int(st.session_state.run_seconds // Ts_sec)
    steps_remaining = max_total_steps - int(st.session_state.tick_count)
    n_steps = max(0, min(batch_steps, steps_remaining))

    for k in range(n_steps):
        if not st.session_state.collecting:
            break

        # Current PV (glucose)
        g_now = float(st.session_state.y[0])

        # Controller (manual or PID Type-B velocity form)
        if st.session_state.mode == "Manual":
            u = float(st.session_state.u_manual)
            u = min(st.session_state.u_hi, max(st.session_state.u_lo, u))
            # keep u_prev in sync so switching to Auto is smooth
            st.session_state.u_prev = u
        else:
            u = pid_typeb_velocity(
                sp=float(st.session_state.g_sp),
                pv=g_now,
                Ts_sec=Ts_sec,
                Kc=float(st.session_state.Kc),
                Ki=float(st.session_state.Ki),
                Kd=float(st.session_state.Kd),
                u_lo=float(st.session_state.u_lo),
                u_hi=float(st.session_state.u_hi),
            )

        # Absolute simulation time for this *new* sample (in hours)
        next_tick = st.session_state.tick_count + 1
        t_elapsed_hr = next_tick * Ts_hr

        # Disturbance evaluated at absolute time
        if st.session_state.meals_on:
            d_k = meal_value_at_time(
                t_elapsed_hr,
                meal_hours=(8.0, 12.0, 18.0),
                A_base=1200.0,
                scale=float(st.session_state.meal_scale),
                tau_decay_hr=1.0
            )
        else:
            d_k = 0.0

        # Integrate plant over one sample with ODEINT (short span: Ts only)
        y0 = st.session_state.y.copy()
        # RHS doesn't use absolute t, so integrate over [0, Ts_hr]
        tspan = [0.0, Ts_hr]  # hours
        y_next = odeint(diabetic_rhs, y0, tspan, args=(u, d_k))
        st.session_state.y = y_next[-1, :]

        # Logging (append with absolute time)
        st.session_state.t_log.append(t_elapsed_hr)
        st.session_state.g_log.append(st.session_state.y[0])
        st.session_state.sp_log.append(st.session_state.g_sp)
        st.session_state.u_log.append(u)
        st.session_state.mode_log.append(st.session_state.mode)
        st.session_state.d_log.append(d_k)

        # Increment absolute tick counter
        st.session_state.tick_count = next_tick

        # Build DataFrames for live charts
        df_top = pd.DataFrame({
            "Time (hr)": st.session_state.t_log,
            "Glucose": st.session_state.g_log,
            "SetPoint": st.session_state.sp_log,
            "Lower Limit (65)": [65.0]*len(st.session_state.t_log),
            "Upper Limit (104)": [104.0]*len(st.session_state.t_log),
        }).set_index("Time (hr)")

        df_mid = pd.DataFrame({
            "Time (hr)": st.session_state.t_log,
            "Insulin (mU/min)": st.session_state.u_log,
        }).set_index("Time (hr)")

        df_bot = pd.DataFrame({
            "Time (hr)": st.session_state.t_log,
            "Meal Disturbance": st.session_state.d_log,
        }).set_index("Time (hr)")

        # Plot glucose & SP and limits
        chart_top.line_chart(df_top[["Lower Limit (65)", "Glucose", "SetPoint", "Upper Limit (104)"]])

        # Insulin chart
        chart_mid.line_chart(df_mid)

        # Disturbance chart
        if st.session_state.meals_on:
            chart_bot.area_chart(df_bot)
        else:
            chart_bot.write("Meal disturbances disabled.")

        # Status
        status.info(
            f"t={t_elapsed_hr:5.2f} hr | g={st.session_state.y[0]:.1f} mg/dL → SP={st.session_state.g_sp:.1f} | "
            f"u={u:.3f} mU/min | mode={st.session_state.mode}"
        )

        # Keep UI responsive (you can reduce this if you want faster sim)
        time.sleep(0.2)

    # If we've reached the overall cap, stop
    if st.session_state.tick_count >= max_total_steps:
        st.session_state.collecting = False
        st.warning("Reached maximum configured run length. Press Start to begin a new run.")

# -----------------------------------------------------------------------------
# Download log as CSV
# -----------------------------------------------------------------------------
if len(st.session_state.t_log) > 0:
    df_out = pd.DataFrame({
        "Time (hr)": st.session_state.t_log,
        "Glucose (mg/dL)": st.session_state.g_log,
        "SetPoint (mg/dL)": st.session_state.sp_log,
        "Insulin (mU/min)": st.session_state.u_log,
        "Mode": st.session_state.mode_log,
        "Meal Disturbance": st.session_state.d_log,
        "Kc": [st.session_state.Kc]*len(st.session_state.t_log),
        "Ki (1/min)": [st.session_state.Ki]*len(st.session_state.t_log),
        "Kd (min)": [st.session_state.Kd]*len(st.session_state.t_log),
    })
    st.subheader("Download Data")
    st.download_button(
        "Download CSV",
        data=df_out.to_csv(index=False),
        file_name="glucose_pid_data.csv",
        mime="text/csv",
    )
else:
    st.write("No data yet. Choose mode, set SP or insulin rate, then press **Start**.")
