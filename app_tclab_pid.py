import streamlit as st
import pandas as pd
import numpy as np
import time
import tclab

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(page_title="TCLab PID Control", layout="wide")
st.title("TCLab PID Control")
st.caption("See https://apmonitor.com/heat.htm for additional TCLab information.")

# ---------------------------
# Hardware Toggle (uncomment if running locally with USB)
# ---------------------------
hardware = False
# tclab_hardware = st.sidebar.checkbox("Use TCLab hardware", value=False)
# hardware = bool(tclab_hardware)

# ---------------------------
# Helpers to seed defaults (avoid widget/session_state conflict)
# ---------------------------
def ensure_default(name, val):
    if name not in st.session_state:
        st.session_state[name] = val

def init_state():
    # Control state
    ensure_default("collecting_data", False)
    ensure_default("started_once", False)
    ensure_default("lab", None)
    ensure_default("start_time", None)

    # Controller internals
    ensure_default("prev_T1", None)
    ensure_default("prev_T2", None)
    ensure_default("I1", 0.0)
    ensure_default("I2", 0.0)

    # Logs
    ensure_default("timestamps", [])
    ensure_default("time_s", [])
    ensure_default("T1_list", [])
    ensure_default("T2_list", [])
    ensure_default("Q1_list", [])
    ensure_default("Q2_list", [])
    ensure_default("SP1_list", [])
    ensure_default("SP2_list", [])
    ensure_default("elapsed", 0)

    # Widget defaults (seed once; widgets will only use key=, no value=)
    ensure_default("SP1", 35)
    ensure_default("SP2", 30)
    ensure_default("KP1", 2.0)
    ensure_default("KI1", 0.02)
    ensure_default("KD1", 0.0)     # default derivative OFF
    ensure_default("KP2", 3.0)
    ensure_default("KI2", 0.03)
    ensure_default("KD2", 0.0)     # default derivative OFF
    ensure_default("sample_time", 1.0)
    ensure_default("run_seconds", 600)
    

init_state()

# ---------------------------
# Sidebar Controls (widgets write directly to session_state)
# ---------------------------
st.sidebar.title("PID Setpoints")
st.sidebar.slider("T1 Setpoint (°C)", 25, 75, key="SP1")
st.sidebar.slider("T2 Setpoint (°C)", 25, 75, key="SP2")

st.sidebar.image("tclab.png", caption="Temperature Control Lab", use_container_width=True)

st.sidebar.subheader("T1 PID")
st.sidebar.number_input("KP₁", min_value=0.0, step=0.1, key="KP1")
st.sidebar.number_input("KI₁ (1/s)", min_value=0.0, step=0.01, key="KI1")
st.sidebar.number_input("KD₁ (s)", min_value=0.0, step=1.0, key="KD1")

st.sidebar.markdown("---")
st.sidebar.subheader("T2 PID")
st.sidebar.number_input("KP₂", min_value=0.0, step=0.1, key="KP2")
st.sidebar.number_input("KI₂ (1/s)", min_value=0.0, step=0.01, key="KI2")
st.sidebar.number_input("KD₂ (s)", min_value=0.0, step=1.0, key="KD2")

st.sidebar.markdown("---")
st.sidebar.number_input("Sample Time (s)", min_value=0.1, step=0.1, key="sample_time")
st.sidebar.number_input("Run Duration (s)", min_value=10, step=10, key="run_seconds")

if hardware:
    LED = st.sidebar.slider("LED Brightness (%)", 0, 100, 0)

# ---------------------------
# PID (Type B / derivative on measurement) with anti-windup
# ---------------------------
def pid_type_b(sp, pv, dt, kp, ki, kd, integ_prev, pv_prev):
    """
    Parallel PID (non-interacting):
      u = kp*e + I + D, where D = -kp*kd*d(pv)/dt  (derivative on measurement)
    Output saturated to [0,100] with conditional integration anti-windup.
    """
    e = sp - pv
    if pv_prev is None or dt <= 0:
        d_pv = 0.0
    else:
        d_pv = (pv - pv_prev) / dt

    P = kp * e
    D = -kp * kd * d_pv
    I_candidate = integ_prev + ki * e * dt
    u_unsat = P + I_candidate + D

    # Saturate
    u_sat = min(100.0, max(0.0, u_unsat))

    # Conditional integration to avoid windup
    if (u_unsat > 100.0 and e > 0) or (u_unsat < 0.0 and e < 0):
        I_new = integ_prev
        u_sat = min(100.0, max(0.0, P + integ_prev + D))
    else:
        I_new = I_candidate

    return u_sat, I_new

# ---------------------------
# Buttons
# ---------------------------
left, mid, _ = st.columns([1,1,1])
with left:
    if st.button("Start PID Control"):
        # Reset logs and internals ONLY on Start
        st.session_state.collecting_data = True
        st.session_state.timestamps = []
        st.session_state.time_s = []
        st.session_state.T1_list = []
        st.session_state.T2_list = []
        st.session_state.Q1_list = []
        st.session_state.Q2_list = []
        st.session_state.SP1_list = []
        st.session_state.SP2_list = []
        st.session_state.prev_T1 = None
        st.session_state.prev_T2 = None
        st.session_state.I1 = 0.0
        st.session_state.I2 = 0.0
        st.session_state.elapsed = 0.0

        # Create lab
        if hardware:
            TCLab = tclab.setup(connected=True)
            st.session_state.lab = TCLab()
        else:
            TCLab = tclab.setup(connected=False, speedup=10)
            st.session_state.lab = TCLab()

        st.session_state.started_once = True
        st.session_state.start_time = time.time()

with mid:
    if st.button("Stop"):
        if st.session_state.collecting_data:
            st.session_state.collecting_data = False
        if st.session_state.lab is not None:
            try:
                st.session_state.lab.close()
            except Exception:
                pass

# ---------------------------
# Chart placeholders (Streamlit trends)
# ---------------------------
top_chart = st.empty()     # SP1, T1, SP2, T2
bottom_chart = st.empty()  # Q1, Q2
status_placeholder = st.empty()

# ---------------------------
# Control + Logging Loop
# ---------------------------
if st.session_state.collecting_data and st.session_state.lab is not None:
    start_time = st.session_state.get("start_time", time.time())
    if hardware:
        t_prev = time.time()

    with st.session_state.lab:
        for _ in tclab.clock(int(st.session_state.run_seconds)):
            if not st.session_state.collecting_data:
                break

            now = time.time()
            if hardware:
                dt = now - t_prev
                if dt <= 0:
                    dt = st.session_state.sample_time
                t_prev = now
            else:
                elapsed = st.session_state.elapsed
                dt = st.session_state.sample_time

            # Read PVs
            T1 = st.session_state.lab.T1
            T2 = st.session_state.lab.T2

            # Compute PIDs
            Q1, st.session_state.I1 = pid_type_b(
                sp=st.session_state.SP1, pv=T1, dt=dt,
                kp=st.session_state.KP1, ki=st.session_state.KI1, kd=st.session_state.KD1,
                integ_prev=st.session_state.I1, pv_prev=st.session_state.prev_T1
            )
            Q2, st.session_state.I2 = pid_type_b(
                sp=st.session_state.SP2, pv=T2, dt=dt,
                kp=st.session_state.KP2, ki=st.session_state.KI2, kd=st.session_state.KD2,
                integ_prev=st.session_state.I2, pv_prev=st.session_state.prev_T2
            )

            # Apply outputs
            st.session_state.lab.Q1(Q1)
            st.session_state.lab.Q2(Q2)
            if hardware:
                st.session_state.lab.LED(0)

            # Append logs
            if hardware:
                elapsed = int(now - start_time)
            else:
                elapsed += st.session_state.sample_time
            st.session_state.elapsed = elapsed
            st.session_state.timestamps.append(now)
            st.session_state.time_s.append(elapsed)
            st.session_state.T1_list.append(T1)
            st.session_state.T2_list.append(T2)
            st.session_state.Q1_list.append(Q1)
            st.session_state.Q2_list.append(Q2)
            st.session_state.SP1_list.append(st.session_state.SP1)
            st.session_state.SP2_list.append(st.session_state.SP2)

            # Update prev PVs
            st.session_state.prev_T1 = T1
            st.session_state.prev_T2 = T2

            # Build dataframes for plotting
            df_top = pd.DataFrame({
                "Time (s)": st.session_state.time_s,
                "SP1 (°C)": st.session_state.SP1_list,
                "T1 (°C)": st.session_state.T1_list,
                "SP2 (°C)": st.session_state.SP2_list,
                "T2 (°C)": st.session_state.T2_list,
            }).set_index("Time (s)")

            df_bot = pd.DataFrame({
                "Time (s)": st.session_state.time_s,
                "Q1 (%)": st.session_state.Q1_list,
                "Q2 (%)": st.session_state.Q2_list,
            }).set_index("Time (s)")

            # Update Streamlit charts
            top_chart.line_chart(df_top[["SP1 (°C)", "T1 (°C)", "SP2 (°C)", "T2 (°C)"]])
            bottom_chart.line_chart(df_bot[["Q1 (%)", "Q2 (%)"]])

            # Status line
            status_placeholder.info(
                f"T1={T1:5.1f}°C → SP1={st.session_state.SP1}°C | Q1={Q1:5.1f}% || "
                f"T2={T2:5.1f}°C → SP2={st.session_state.SP2}°C | Q2={Q2:5.1f}%"
            )

            # Honor chosen sample time
            if hardware:
                sleep_left = st.session_state.sample_time - (time.time() - now)
                if sleep_left > 0:
                    time.sleep(sleep_left)
            else:
                time.sleep(0.1)

        # Close when done
        try:
            st.session_state.lab.close()
        except Exception:
            pass
        st.session_state.collecting_data = False

# ---------------------------
# Download Data
# ---------------------------
if len(st.session_state.time_s) > 0:
    df_out = pd.DataFrame({
        "Time": st.session_state.time_s,
        "SP1": st.session_state.SP1_list,
        "T1": st.session_state.T1_list,
        "Q1": st.session_state.Q1_list,
        "SP2": st.session_state.SP2_list,
        "T2": st.session_state.T2_list,
        "Q2": st.session_state.Q2_list,
    })
    st.subheader("Download Data")
    csv = df_out.to_csv(index=False)
    st.download_button(
        label="Download Data as CSV",
        data=csv,
        file_name="tclab_pid_data.csv",
        mime="text/csv"
    )
else:
    st.write("No data collected yet. Press **Start PID Control**.")
