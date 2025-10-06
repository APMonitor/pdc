"""Streamlit application for exothermic CSTR temperature control.

This app provides an interactive simulation of an exothermic
continuous stirred‑tank reactor (CSTR) where the temperature of
the cooling jacket is manipulated to control the reactor
temperature.  Users can operate the process in either manual
mode (specifying a fixed coolant temperature) or automatic
mode using a PID controller.  The simulation integrates the
two state variables – concentration of reactant A and reactor
temperature – with a simple forward Euler scheme.  Logging and
plotting of results allow real‑time visualisation of process
behaviour.

References:
The model equations implemented here follow the mole and energy
balances given in the assignment.  With volumetric flowrate q, reactor
volume V, mixture density ρ and heat capacity Cₚ, the dynamic model is

```
dcA/dt = (q/V)(cAf − cA) − k(T) cA
dT/dt  = (q/V)(Tₙ − T) + ΔH/(ρ Cₚ) k(T) cA + (UA)/(V ρ Cₚ)(Tc − T)
```

where k(T) = k₀ exp(−E/(R T)) is the Arrhenius rate constant.  All
parameter values are consistent with the problem statement, including
the volumetric flowrate (q = 100 m³/s).  The controller implementation
follows the Type‑B discrete PID formulation described
in the Dynamics and Control notes. See https://apmonitor.com/pdc
"""

import streamlit as st
import pandas as pd
import numpy as np
import time
import altair as alt

# ---------------------------------------------------------------------------
# Page configuration and title
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Exothermic CSTR Control", layout="wide")
st.title("Exothermic CSTR PID Control")
st.caption(
    "Adjust Cooling Jacket Temperature to Avoid Reactor Temperature Run-away (<400K) and Lower Concentration Below 0.1"
)

# ---------------------------------------------------------------------------
# Defaults & Session State helpers
#
# The ensure_default() helper sets a default value on the first run of the
# application and avoids overwriting existing session_state entries on
# subsequent runs.  init_state() populates all stateful variables used
# throughout the simulation, including process states, controller memory
# and logging lists.  These variables persist across reruns while the
# session remains open.
# ---------------------------------------------------------------------------
def ensure_default(name, val):
    """Initialise a session state value if it is not already present."""
    if name not in st.session_state:
        st.session_state[name] = val


def init_state():
    """Set all default values required for simulation and control."""
    # Control flags and timing
    ensure_default("collecting_data", False)
    ensure_default("started_once", False)
    ensure_default("start_time", None)

    # Plant state variables: concentration of A (mol/m^3) and temperature (K).
    # The default values correspond to a typical steady state of the system.
    ensure_default("Ca", 0.87725294608097)  # Steady‑state concentration
    ensure_default("T", 324.475443431599)   # Steady‑state temperature

    # Controller internals: integral term and previous temperature for derivative
    ensure_default("I", 0.0)
    ensure_default("prev_T", None)

    # PID Type‑B internals: previous output and error history for velocity form
    # u_prev stores the previous controller output (coolant temperature) to
    # compute the incremental change.  error_prev stores the previous error.
    # pv_prev and pv_prev2 store the previous two process variable values for
    # computing the discrete second derivative of the PV in the derivative term.
    ensure_default("u_prev", 300.0)       # previous output (coolant temperature)
    ensure_default("error_prev", None)    # previous control error
    ensure_default("pv_prev", None)       # previous process variable (temperature)
    ensure_default("pv_prev2", None)      # two‑steps prior PV

    # Logging lists for plotting and data export
    ensure_default("t_log", [])
    ensure_default("Ca_log", [])
    ensure_default("T_log", [])
    ensure_default("sp_log", [])
    ensure_default("Tc_log", [])
    ensure_default("mode_log", [])

    # UI seeds (widgets reference these keys directly)
    ensure_default("mode", "Automatic (PID)")        # Control mode
    ensure_default("SP_T", 324.0)                    # Reactor temperature setpoint (K)
    ensure_default("Kc", 2.0)                         # Controller gain
    ensure_default("Ki", 0.05)                        # Integral gain (1/min)
    ensure_default("Kd", 0.0)                          # Derivative gain (min)
    ensure_default("Tc_manual", 300.0)                 # Manual coolant temperature (K)
    # Bounds on coolant temperature
    ensure_default("Tc_min", 250.0)
    ensure_default("Tc_max", 350.0)
    # Simulation timing
    # Sample time in seconds (0.1 s by default)
    ensure_default("sample_time", 0.1)
    ensure_default("run_seconds", 600)                 # Number of loop iterations (max)


init_state()

# ---------------------------------------------------------------------------
# Sidebar controls
#
# The sidebar collects all user inputs: control mode, setpoint, manual
# coolant temperature, PID tuning parameters, simulation timing and
# optional image.  Keys correspond directly to entries in st.session_state.
# ---------------------------------------------------------------------------
st.sidebar.title("Controls")

# Mode selection (Manual or Automatic PID)
st.sidebar.radio("Mode", options=["Automatic (PID)", "Manual"], key="mode")

# Setpoint input (reactor temperature)
st.sidebar.slider(
    "Reactor Temperature Setpoint (K)",
    min_value=250.0,
    max_value=400.0,
    key="SP_T",
    step=1.0,
)

if st.session_state.mode == "Manual":
    # In manual mode the user sets the cooling jacket temperature directly.
    st.sidebar.slider(
        "Cooling Jacket Temperature (Manual) [K]",
        min_value=float(st.session_state.Tc_min),
        max_value=float(st.session_state.Tc_max),
        key="Tc_manual",
        step=1.0,
    )
else:
    # PID tuning inputs
    st.sidebar.subheader("PID Tuning Parameters")
    st.sidebar.number_input(
        "Kc (gain)",
        min_value=0.0,
        step=0.1,
        key="Kc",
    )
    st.sidebar.number_input(
        "Ki (1/min)",
        min_value=0.0,
        step=0.01,
        key="Ki",
    )
    st.sidebar.number_input(
        "Kd (min)",
        min_value=0.0,
        step=0.01,
        key="Kd",
    )

# Allow the user to adjust simulation timing
st.sidebar.number_input(
    "Sample Time (s)",
    min_value=0.1,
    step=0.1,
    key="sample_time",
)
st.sidebar.number_input(
    "Run Duration (s)",
    min_value=10,
    step=10,
    key="run_seconds",
)

# Display a schematic if available
try:
    st.sidebar.image("cstr_schematic.png", caption="CSTR Schematic", use_container_width=True)
except Exception:
    pass

# ---------------------------------------------------------------------------
# Start/Stop buttons
#
# Two buttons allow the user to start a new simulation run or stop an
# ongoing run.  Starting a run resets all logs and controller memory.
# ---------------------------------------------------------------------------
colA, colB, _ = st.columns([1, 1, 2])
with colA:
    if st.button("Start"):
        # Reset logs and controller internals on each start
        st.session_state.collecting_data = True
        st.session_state.t_log = []
        st.session_state.Ca_log = []
        st.session_state.T_log = []
        st.session_state.sp_log = []
        st.session_state.Tc_log = []
        st.session_state.mode_log = []
        st.session_state.I = 0.0
        st.session_state.prev_T = None
        # Reset Type‑B PID internals
        st.session_state.u_prev = float(st.session_state.Tc_manual)
        st.session_state.error_prev = None
        st.session_state.pv_prev = None
        st.session_state.pv_prev2 = None
        st.session_state.start_time = time.time()
        st.session_state.started_once = True

with colB:
    if st.button("Stop"):
        st.session_state.collecting_data = False

# ---------------------------------------------------------------------------
# CSTR dynamics
#
# The cstr_rates() function returns the derivatives of Ca and T given
# current states and coolant temperature.  It implements the mole and
# energy balance equations summarised earlier.
# The constants here are chosen for consistency with the examples in the
# literature.
# ---------------------------------------------------------------------------
def cstr_rates(Ca, T, Tc):
    """Compute concentration and temperature derivatives for the CSTR.

    Parameters
    ----------
    Ca : float
        Concentration of A (mol/m^3).
    T : float
        Reactor temperature (K).
    Tc : float
        Cooling jacket temperature (K), manipulated variable.

    Returns
    -------
    tuple of floats
        (dCadt, dTdt) in units of (mol/m^3/min, K/min).
    """
    # Physical and kinetic constants
    # Use the same parameter values as the problem statement.  The
    # volumetric flowrate q is nominally 100 m³/s (or 100 in arbitrary
    # units) and the model is expressed in minutes, so there is an
    # implicit unit conversion when dt is converted to minutes.
    q = 100.0        # volumetric flowrate (m^3/s) – consistent with problem
    V = 100.0        # reactor volume (m^3)
    rho = 1000.0     # density (kg/m^3)
    Cp = 0.239       # heat capacity (J/kg-K)
    mdelH = 5.0e4    # heat of reaction for A->B (J/mol), positive for exothermic
    EoverR = 8750.0  # E/R (1/K) for Arrhenius expression
    k0 = 7.2e10      # pre-exponential factor (1/min)
    UA = 5.0e4       # overall heat transfer coefficient * area (J/min-K)
    Tf = 350.0       # feed temperature (K)
    Caf = 1.0        # feed concentration (mol/m^3)

    # Reaction rate constant using Arrhenius law
    k = k0 * np.exp(-EoverR / T)
    # Reaction rate per unit volume
    rA = k * Ca

    # Mole balance: dCadt
    dCadt = (q / V) * (Caf - Ca) - rA
    # Energy balance: dTdt
    dTdt = (q / V) * (Tf - T) + (mdelH / (rho * Cp)) * rA + (UA / (V * rho * Cp)) * (Tc - T)
    return dCadt, dTdt


def step_sim(dt_sec, Tc_input):
    """Advance the CSTR state by one sample using explicit Euler integration.

    The sample time dt_sec is specified in seconds and converted to
    minutes to match the units of the kinetic model.  State variables
    (Ca and T) stored in st.session_state are updated in place.
    """
    dt_min = dt_sec / 60.0
    Ca_current = st.session_state.Ca
    T_current = st.session_state.T
    dCadt, dTdt = cstr_rates(Ca_current, T_current, Tc_input)
    # Euler integration
    Ca_next = Ca_current + dCadt * dt_min
    T_next = T_current + dTdt * dt_min
    # Apply simple bounds: concentration cannot be negative
    st.session_state.Ca = max(0.0, Ca_next)
    st.session_state.T = T_next


def pid_typeb_compute(sp: float, pv: float, dt_sec: float, kc: float, ki: float, kd: float) -> float:
    """Discrete Type‑B PID controller in velocity form with anti‑reset windup.

    This implementation follows the velocity (incremental) formulation
    recommended for Type‑B PID control【450933523291993†L149-L172】.  The setpoint
    is removed from the derivative term to eliminate derivative kick.  The
    controller increment is composed of a proportional change based on the
    change in error, an integral term based on the current error, and a
    derivative term based on the second finite difference of the process
    variable.  Anti‑reset windup is enforced by freezing the integral
    contribution when the tentative controller output would exceed the
    actuator limits and the sign of the error would drive it further
    into saturation.

    Parameters
    ----------
    sp : float
        Setpoint for the reactor temperature (K).
    pv : float
        Current process variable (reactor temperature, K).
    dt_sec : float
        Sample time in seconds.
    kc : float
        Proportional gain.
    ki : float
        Integral gain (1/min).
    kd : float
        Derivative gain (min).

    Returns
    -------
    float
        New coolant jacket temperature (K) after applying saturation.
    """
    # Convert sampling period to minutes
    dt_min = dt_sec / 60.0
    # Initialize history variables on the first call
    if st.session_state.error_prev is None:
        st.session_state.error_prev = sp - pv
    if st.session_state.pv_prev is None:
        st.session_state.pv_prev = pv
    if st.session_state.pv_prev2 is None:
        st.session_state.pv_prev2 = pv

    # Current error
    error = sp - pv
    # Proportional incremental term based on error change
    P_inc = kc * (error - st.session_state.error_prev)
    # Integral incremental term candidate
    I_inc_candidate = ki * error * dt_min
    # Derivative incremental term based on second difference of PV
    # Negative sign implements derivative on measurement
    D_inc = -kd * ((pv - 2.0 * st.session_state.pv_prev + st.session_state.pv_prev2) / dt_min)
    # Tentative controller output prior to applying limits
    u_proposed = st.session_state.u_prev + P_inc + I_inc_candidate + D_inc
    # Saturation limits
    u_lo = float(st.session_state.Tc_min)
    u_hi = float(st.session_state.Tc_max)
    # Anti‑reset windup: skip integral term if output is beyond limits and
    # the current error would drive the output further into saturation
    if (u_proposed > u_hi and error > 0.0) or (u_proposed < u_lo and error < 0.0):
        I_inc = 0.0
        u_unsat = st.session_state.u_prev + P_inc + I_inc + D_inc
    else:
        I_inc = I_inc_candidate
        u_unsat = u_proposed
    # Apply actuator limits
    u_new = min(u_hi, max(u_lo, u_unsat))
    # Update historical states for next iteration
    st.session_state.error_prev = error
    st.session_state.pv_prev2 = st.session_state.pv_prev
    st.session_state.pv_prev = pv
    st.session_state.u_prev = u_new
    return u_new


# ---------------------------------------------------------------------------
# Placeholder objects for plots and status
#
# Streamlit's dynamic rendering requires that charts be created with st.empty().
# They can then be updated in the loop.  The status block prints current
# values for rapid inspection.
# ---------------------------------------------------------------------------
top_chart = st.empty()      # For Ca, T and SP
bottom_chart = st.empty()   # For coolant jacket temperature
status = st.empty()

# ---------------------------------------------------------------------------
# Main simulation loop
#
# When collecting_data is True the app enters a timed loop.  At each
# iteration the controller calculates a new coolant temperature (or
# uses the manual setting) and the plant state is advanced.  Data
# are logged and plots updated.  The loop terminates either when
# collecting_data is cleared (by Stop) or when run_seconds iterations
# have completed.
# ---------------------------------------------------------------------------
if st.session_state.collecting_data:
    start_time = st.session_state.start_time or time.time()
    # Use a previous time marker for pacing sleep
    t_prev = time.time()
    # Number of iterations is limited by run_seconds to avoid infinite loops
    for _ in range(int(st.session_state.run_seconds)):
        if not st.session_state.collecting_data:
            break

        # Determine dt based on sample_time – ignore actual wall clock for model update
        dt_sec = float(st.session_state.sample_time)

        # Controller / Manual calculation of coolant temperature
        if st.session_state.mode == "Manual":
            Tc = float(st.session_state.Tc_manual)
        else:
            Tc = pid_typeb_compute(
                sp=float(st.session_state.SP_T),
                pv=float(st.session_state.T),
                dt_sec=dt_sec,
                kc=float(st.session_state.Kc),
                ki=float(st.session_state.Ki),
                kd=float(st.session_state.Kd),
            )

        # Advance plant state using explicit Euler integration
        step_sim(dt_sec, Tc)
        # Stop the simulation if the reactor temperature exceeds 400 K
        if st.session_state.T > 400.0:
            st.session_state.collecting_data = False
            st.error(
                "Runaway reactor detected: temperature exceeds 400 K. Simulation stopped."
            )
            break

        # Append logs
        elapsed = int(time.time() - start_time)
        st.session_state.t_log.append(elapsed)
        st.session_state.Ca_log.append(st.session_state.Ca)
        st.session_state.T_log.append(st.session_state.T)
        st.session_state.sp_log.append(st.session_state.SP_T)
        st.session_state.Tc_log.append(Tc)
        st.session_state.mode_log.append(st.session_state.mode)

        # Prepare data frames for plotting using Altair
        # Combine temperature and set point traces
        df_temp = pd.DataFrame(
            {
                "Time": st.session_state.t_log,
                "CoolingTemp": st.session_state.Tc_log,
                "ReactorTemp": st.session_state.T_log,
                "SetPoint": st.session_state.sp_log,
            }
        )
        df_temp_melt = df_temp.melt("Time", var_name="variable", value_name="value")
        chart_temp = (
            alt.Chart(df_temp_melt)
            .mark_line()
            .encode(
                x=alt.X("Time", title="Time (s)"),
                y=alt.Y(
                    "value",
                    title="Temperature (K)",
                    scale=alt.Scale(domain=[250, 400]),
                ),
                color=alt.Color(
                    "variable:N",
                    scale=alt.Scale(
                        domain=["CoolingTemp", "ReactorTemp", "SetPoint"],
                        range=["blue", "red", "green"],
                    ),
                    legend=alt.Legend(title=""),
                ),
            )
            .properties(height=250)
        )
        # Concentration plot with target level
        df_conc = pd.DataFrame(
            {
                "Time": st.session_state.t_log,
                "Concentration": st.session_state.Ca_log,
                "TargetConc": [0.1] * len(st.session_state.t_log),
            }
        )
        df_conc_melt = df_conc.melt("Time", var_name="variable", value_name="value")
        chart_conc = (
            alt.Chart(df_conc_melt)
            .mark_line()
            .encode(
                x=alt.X("Time", title="Time (s)"),
                y=alt.Y(
                    "value",
                    title="Concentration (mol/m^3)",
                    scale=alt.Scale(domain=[0, 1]),
                ),
                color=alt.Color(
                    "variable:N",
                    scale=alt.Scale(
                        domain=["Concentration", "TargetConc"],
                        range=["blue", "red"],
                    ),
                    legend=alt.Legend(title=""),
                ),
                strokeDash=alt.StrokeDash(
                    "variable:N",
                    scale=alt.Scale(
                        domain=["Concentration", "TargetConc"],
                        range=[[0], [4, 2]],
                    ),
                ),
            )
            .properties(height=250)
        )
        top_chart.altair_chart(chart_temp, use_container_width=True)
        bottom_chart.altair_chart(chart_conc, use_container_width=True)

        # Update status string
        status.info(
            f"t={elapsed:4d}s | Ca={st.session_state.Ca:.3f} mol/m^3, "
            f"T={st.session_state.T:.2f} K → SP={st.session_state.SP_T:.2f} K | "
            f"Jacket={Tc:.2f} K | Mode={st.session_state.mode}"
        )

        # Pace the loop: subtract model compute time from sample_time
        sleep_left = float(st.session_state.sample_time) - (time.time() - t_prev)
        if sleep_left > 0:
            time.sleep(sleep_left)
        t_prev = time.time()
    # Stop collecting data automatically after run_seconds iterations
    st.session_state.collecting_data = False


# ---------------------------------------------------------------------------
# Download collected data
#
# Once data have been logged, provide the option to download them as a CSV
# file.  The file includes the time series for concentration, temperature,
# setpoint, coolant temperature, mode and PID parameters.
# ---------------------------------------------------------------------------
if len(st.session_state.t_log) > 0:
    df_out = pd.DataFrame(
        {
            "Time (s)": st.session_state.t_log,
            "CaPV": st.session_state.Ca_log,
            "T_PV": st.session_state.T_log,
            "T_SP": st.session_state.sp_log,
            "Tc": st.session_state.Tc_log,
            "Mode": st.session_state.mode_log,
            "Kc": [st.session_state.Kc] * len(st.session_state.t_log),
            "Ki": [st.session_state.Ki] * len(st.session_state.t_log),
            "Kd": [st.session_state.Kd] * len(st.session_state.t_log),
        }
    )
    st.subheader("Download Data")
    st.download_button(
        "Download CSV",
        data=df_out.to_csv(index=False),
        file_name="cstr__data.csv",
        mime="text/csv",
    )
else:
    st.write(
        "No data collected yet. Choose mode, set a setpoint or coolant temperature, "
        "then press **Start** to begin the simulation."
    )
