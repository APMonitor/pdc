import streamlit as st
import pandas as pd
import numpy as np
import time
from math import sqrt

# ---------------------------
# Page setup
# ---------------------------
st.set_page_config(page_title="Two-Tank Level Control", layout="wide")
st.title("Two-Tank Level Control")
st.caption("See https://apmonitor.com/pdc/index.php/Main/LevelControl for additional details.")

# ---------------------------
# Defaults & Session State helpers
# ---------------------------
def ensure_default(name, val):
    if name not in st.session_state:
        st.session_state[name] = val

def init_state():
    # Control flags and timing
    ensure_default("collecting_data", False)
    ensure_default("started_once", False)
    ensure_default("start_time", None)

    # Plant states (levels)
    ensure_default("h1", 0.0)   # Tank 1 level (0..1)
    ensure_default("h2", 0.0)   # Tank 2 level (0..1)

    # Controller internals
    ensure_default("I", 0.0)         # integral term for PID (single-loop on h2)
    ensure_default("prev_h2", None)  # for derivative on measurement

    # Logs
    ensure_default("t_log", [])
    ensure_default("h1_log", [])
    ensure_default("h2_log", [])
    ensure_default("sp_log", [])
    ensure_default("pump_log", [])
    ensure_default("mode_log", [])

    # Widget seeds (widgets will use only key= to avoid conflicts)
    ensure_default("mode", "Automatic (PID)")  # or "Manual"
    ensure_default("SP_h2", 0.5)               # setpoint for lower tank (fraction of full, 0..1)
    ensure_default("Kc", 2.0)
    ensure_default("Ki", 0.03)                 # 1/s
    ensure_default("Kd", 0.0)                  # s (default 0, no derivative)
    ensure_default("pump_manual", 0.2)         # manual pump (0..1)
    ensure_default("valve_split", 0.0)         # 0 -> to top tank, 1 -> to bottom tank
    ensure_default("sample_time", 1.0)         # s
    ensure_default("run_seconds", 600)         # max loop ticks per run

init_state()

# ---------------------------
# Sidebar controls
# ---------------------------
st.sidebar.title("Controls")

# Mode
st.sidebar.radio("Mode", options=["Automatic (PID)", "Manual"], key="mode")

# Setpoint & pump / PID tuning
st.sidebar.slider("Lower Tank Setpoint (h2, fraction full)", 0.0, 1.0, key="SP_h2", step=0.01)

if st.session_state.mode == "Manual":
    st.sidebar.slider("Pump (Manual) [0..1]", 0.0, 1.0, key="pump_manual", step=0.01)
else:
    st.sidebar.subheader("PID")
    st.sidebar.number_input("KP (gain)", min_value=0.0, step=0.1, key="Kc")
    st.sidebar.number_input("KI (1/s)", min_value=0.0, step=0.01, key="Ki")
    st.sidebar.number_input("KD (s)", min_value=0.0, step=0.1, key="Kd")  # default seeded to 0.0

# Image
try:
    st.sidebar.image("2tank.png", caption="Two-Tank Schematic", use_container_width=True)
except Exception:
    pass

st.sidebar.number_input("Sample Time (s)", min_value=0.1, step=0.1, key="sample_time")
st.sidebar.number_input("Run Duration (s)", min_value=10, step=10, key="run_seconds")

# Valve split between tanks (0→all to Tank1, 1→all to Tank2)
st.sidebar.slider("Valve Split to Tank 2 (fraction)", 0.0, 1.0, key="valve_split", step=0.05)

# ---------------------------
# Buttons
# ---------------------------
colA, colB, _ = st.columns([1,1,2])
with colA:
    if st.button("Start"):
        # Reset logs and controller only on Start
        st.session_state.collecting_data = True
        st.session_state.t_log = []
        st.session_state.h1_log = []
        st.session_state.h2_log = []
        st.session_state.sp_log = []
        st.session_state.pump_log = []
        st.session_state.mode_log = []
        st.session_state.I = 0.0
        st.session_state.prev_h2 = None
        st.session_state.start_time = time.time()
        st.session_state.started_once = True

with colB:
    if st.button("Stop"):
        st.session_state.collecting_data = False

# ---------------------------
# Process model (discrete Euler integration)
# ---------------------------
def tank_rates(h1, h2, pump, valve_frac):
    """
    Dual gravity-drained tanks:
      c1 = inlet coefficient, c2 = outlet coefficient
      valve_frac in [0,1]: portion of pump flow routed directly to Tank 2
    """
    c1 = 0.08
    c2 = 0.04
    h1 = max(0.0, h1)
    h2 = max(0.0, h2)

    # Inflow split: (1 - valve) into Tank1, valve into Tank2
    dh1dt = c1 * (1.0 - valve_frac) * pump - c2 * sqrt(h1)
    dh2dt = c1 * valve_frac * pump + c2 * sqrt(h1) - c2 * sqrt(h2)

    # Simple overflow handling: cap growth if full
    if h1 >= 1.0 and dh1dt > 0.0:
        dh1dt = 0.0
    if h2 >= 1.0 and dh2dt > 0.0:
        dh2dt = 0.0
    return dh1dt, dh2dt

def step_sim(dt, pump, valve_frac):
    """Advance plant by one sample using explicit Euler."""
    h1, h2 = st.session_state.h1, st.session_state.h2
    dh1dt, dh2dt = tank_rates(h1, h2, pump, valve_frac)
    h1_next = max(0.0, min(1.0, h1 + dh1dt * dt))
    h2_next = max(0.0, min(1.0, h2 + dh2dt * dt))
    st.session_state.h1, st.session_state.h2 = h1_next, h2_next

# ---------------------------
# PID (parallel, derivative on measurement) + anti-windup
# ---------------------------
def pid_compute(sp, pv, dt, kc, ki, kd):
    """
    u = KP*e + I + D, D = -KD*d(pv)/dt (derivative on measurement)
    Limits: u in [0,1]. Conditional integration anti-windup.
    """
    e = sp - pv
    if st.session_state.prev_h2 is None or dt <= 0:
        d_pv = 0.0
    else:
        d_pv = (pv - st.session_state.prev_h2) / dt

    P = kc * e
    D = -kd * d_pv
    I_candidate = st.session_state.I + ki * e * dt
    u_unsat = P + I_candidate + D

    # Saturate
    u_sat = min(1.0, max(0.0, u_unsat))

    # Conditional anti-windup
    if (u_unsat > 1.0 and e > 0) or (u_unsat < 0.0 and e < 0):
        I_new = st.session_state.I  # freeze
        u_sat = min(1.0, max(0.0, P + st.session_state.I + D))
    else:
        I_new = I_candidate

    st.session_state.I = I_new
    st.session_state.prev_h2 = pv
    return u_sat

# ---------------------------
# Trend placeholders
# ---------------------------
top_chart = st.empty()     # h1, h2, SP(h2)
bottom_chart = st.empty()  # pump
status = st.empty()

# ---------------------------
# Main loop
# ---------------------------
if st.session_state.collecting_data:
    start_time = st.session_state.start_time or time.time()
    t_prev = time.time()

    for _ in range(int(st.session_state.run_seconds)):
        if not st.session_state.collecting_data:
            break

        now = time.time()
        dt = now - t_prev
        if dt <= 0:
            dt = st.session_state.sample_time
        t_prev = now

        # Controller / Manual
        if st.session_state.mode == "Manual":
            pump = float(st.session_state.pump_manual)
        else:
            pump = pid_compute(
                sp=float(st.session_state.SP_h2),
                pv=float(st.session_state.h2),
                dt=float(st.session_state.sample_time),
                kc=float(st.session_state.Kc),
                ki=float(st.session_state.Ki),
                kd=float(st.session_state.Kd),
            )

        # Advance plant
        step_sim(dt=float(st.session_state.sample_time),
                 pump=pump,
                 valve_frac=float(st.session_state.valve_split))

        # Log
        elapsed = int(time.time() - start_time)
        st.session_state.t_log.append(elapsed)
        st.session_state.h1_log.append(st.session_state.h1)
        st.session_state.h2_log.append(st.session_state.h2)
        st.session_state.sp_log.append(st.session_state.SP_h2)
        st.session_state.pump_log.append(pump)
        st.session_state.mode_log.append(st.session_state.mode)

        # Build frames for charts
        df_top = pd.DataFrame({
            "Time (s)": st.session_state.t_log,
            "h1": st.session_state.h1_log,
            "h2": st.session_state.h2_log,
            "SP(h2)": st.session_state.sp_log,
        }).set_index("Time (s)")

        df_bot = pd.DataFrame({
            "Time (s)": st.session_state.t_log,
            "Pump": st.session_state.pump_log,
        }).set_index("Time (s)")

        top_chart.line_chart(df_top[["h1", "h2", "SP(h2)"]])
        bottom_chart.line_chart(df_bot[["Pump"]])

        status.info(
            f"t={elapsed:4d}s | h1={st.session_state.h1:0.3f}, "
            f"h2={st.session_state.h2:0.3f} → SP={st.session_state.SP_h2:0.3f} | "
            f"Pump={pump:0.3f} | Mode={st.session_state.mode} | Valve→T2={st.session_state.valve_split:0.2f}"
        )

        # pace the loop
        sleep_left = st.session_state.sample_time - (time.time() - now)
        if sleep_left > 0:
            time.sleep(sleep_left)

    # stop after run_seconds
    st.session_state.collecting_data = False

# ---------------------------
# Download data
# ---------------------------
if len(st.session_state.t_log) > 0:
    df_out = pd.DataFrame({
        "Time": st.session_state.t_log,
        "h1PV": st.session_state.h1_log,
        "h2PV": st.session_state.h2_log,
        "h2SP": st.session_state.sp_log,
        "Pump": st.session_state.pump_log,
        "Mode": st.session_state.mode_log,
        "Valve": [st.session_state.valve_split]*len(st.session_state.t_log),
        "KP": [st.session_state.Kc]*len(st.session_state.t_log),
        "KI": [st.session_state.Ki]*len(st.session_state.t_log),
        "KD": [st.session_state.Kd]*len(st.session_state.t_log)
    })
    st.subheader("Download Data")
    st.download_button(
        "Download CSV",
        data=df_out.to_csv(index=False),
        file_name="two_tank_level_data.csv",
        mime="text/csv",
    )
else:
    st.write("No data collected yet. Choose mode, set SP or pump, then press **Start**.")
