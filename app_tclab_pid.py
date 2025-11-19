import streamlit as st
import pandas as pd
import numpy as np
import time
import tclab

st.set_page_config(page_title="TCLab PID Control", layout="wide")
st.title("TCLab PID Control")

# ------------------------------
# CONFIG
# ------------------------------
hardware = False

# ------------------------------
# STATE INIT
# ------------------------------
def ensure(k, v):
    if k not in st.session_state:
        st.session_state[k] = v

ensure("collecting", False)
ensure("lab", None)
ensure("last_time", None)

# data logs
ensure("t", [])
ensure("T1", [])
ensure("T2", [])
ensure("Q1", [])
ensure("Q2", [])
ensure("SP1_log", [])
ensure("SP2_log", [])

# controller state
ensure("I1", 0.0)
ensure("I2", 0.0)
ensure("prev_T1", None)
ensure("prev_T2", None)

# UI defaults
ensure("SP1", 35)
ensure("SP2", 30)
ensure("Kc1", 2.0)
ensure("Ki1", 0.02)
ensure("Kd1", 0.0)
ensure("Kc2", 3.0)
ensure("Ki2", 0.03)
ensure("Kd2", 0.0)
ensure("LED", 0)
ensure("sample", 1.0)
ensure("duration", 600.0)

# ------------------------------
# SIDEBAR
# ------------------------------
st.sidebar.header("Setpoints")
st.session_state.SP1 = st.sidebar.slider("T1 Setpoint", 25, 80, st.session_state.SP1)
st.session_state.SP2 = st.sidebar.slider("T2 Setpoint", 25, 80, st.session_state.SP2)

st.sidebar.header("T1 PID")
st.session_state.Kc1 = st.sidebar.number_input(
    "Kc1", min_value=0.0, max_value=10.0, value=float(st.session_state.Kc1), step=0.1
)
st.session_state.Ki1 = st.sidebar.number_input(
    "Ki1", min_value=0.0, max_value=1.0, value=float(st.session_state.Ki1), step=0.01
)
st.session_state.Kd1 = st.sidebar.number_input(
    "Kd1", min_value=0.0, max_value=10.0, value=float(st.session_state.Kd1), step=0.1
)

st.sidebar.header("T2 PID")
st.session_state.Kc2 = st.sidebar.number_input(
    "Kc2", min_value=0.0, max_value=10.0, value=float(st.session_state.Kc2), step=0.1
)
st.session_state.Ki2 = st.sidebar.number_input(
    "Ki2", min_value=0.0, max_value=1.0, value=float(st.session_state.Ki2), step=0.01
)
st.session_state.Kd2 = st.sidebar.number_input(
    "Kd2", min_value=0.0, max_value=10.0, value=float(st.session_state.Kd2), step=0.1
)

st.sidebar.header("Other")
st.session_state.LED = st.sidebar.slider("LED (%)", 0, 100, st.session_state.LED)
st.session_state.sample = st.sidebar.number_input(
    "Sample Time (s)",
    min_value=0.1,
    max_value=10.0,
    value=float(st.session_state.sample),
    step=0.1,
)
st.session_state.duration = st.sidebar.number_input(
    "Run Duration (s)",
    min_value=10.0,
    max_value=2000.0,
    value=float(st.session_state.duration),
    step=10.0,
)

url = "https://apmonitor.com/pdc/uploads/Main/tclab_transparent.png"
try:
    st.sidebar.image(url, caption="TCLab Device")
except Exception:
    pass

# ------------------------------
# START / STOP
# ------------------------------
start = st.button("Start")
stop = st.button("Stop")

def close_lab():
    if st.session_state.lab:
        try:
            st.session_state.lab.Q1(0)
            st.session_state.lab.Q2(0)
            if hardware:
                st.session_state.lab.LED(0)
        except Exception:
            pass
        try:
            st.session_state.lab.close()
        except Exception:
            pass
        st.session_state.lab = None

if stop:
    st.session_state.collecting = False
    close_lab()

if start and not st.session_state.collecting:
    close_lab()

    if hardware:
        L = tclab.setup(connected=True)
    else:
        L = tclab.setup(connected=False, speedup=5)

    st.session_state.lab = L()

    # reset logs
    st.session_state.t = []
    st.session_state.T1 = []
    st.session_state.T2 = []
    st.session_state.Q1 = []
    st.session_state.Q2 = []
    st.session_state.SP1_log = []
    st.session_state.SP2_log = []

    # reset controller
    st.session_state.I1 = 0.0
    st.session_state.I2 = 0.0
    st.session_state.prev_T1 = None
    st.session_state.prev_T2 = None

    st.session_state.start = time.time()
    st.session_state.last_time = None
    st.session_state.collecting = True

# ------------------------------
# PERSISTENT CHARTS FIRST
# ------------------------------
st.subheader("Temperatures / Setpoints")
temp_chart = st.empty()

st.subheader("Heater Outputs")
heat_chart = st.empty()

if len(st.session_state.t) > 0:
    df_top = pd.DataFrame({
        "Time": st.session_state.t,
        "SP1": st.session_state.SP1_log,
        "T1": st.session_state.T1,
        "SP2": st.session_state.SP2_log,
        "T2": st.session_state.T2,
    }).set_index("Time")

    df_bot = pd.DataFrame({
        "Time": st.session_state.t,
        "Q1": st.session_state.Q1,
        "Q2": st.session_state.Q2,
    }).set_index("Time")

    temp_chart.line_chart(df_top)
    heat_chart.line_chart(df_bot)
else:
    st.info("Press Start to begin PID control.")

# ------------------------------
# PID CONTROLLER (ONE STEP)
# ------------------------------
def pid_step(sp, pv, dt, kc, ki, kd, I_prev, pv_prev):
    e = sp - pv
    d = 0 if pv_prev is None else (pv - pv_prev) / dt
    P = kc * e
    I = I_prev + ki * e * dt
    D = -kc * kd * d
    u = P + I + D
    u_sat = min(100, max(0, u))
    if (u > 100 and e > 0) or (u < 0 and e < 0):
        I = I_prev
        u_sat = min(100, max(0, P + I_prev + D))
    return u_sat, I

# ------------------------------
# EXECUTE ONE CONTROL STEP
# ------------------------------
if st.session_state.collecting and st.session_state.lab:
    now = time.time()
    elapsed = now - st.session_state.start

    # stop automatically
    if elapsed >= st.session_state.duration:
        st.session_state.collecting = False
        close_lab()
    else:
        last = st.session_state.last_time
        if last is None or (now - last) >= st.session_state.sample:
            dt = st.session_state.sample if last is None else (now - last)
            st.session_state.last_time = now

            try:
                try:
                    T1 = st.session_state.lab.T1
                    T2 = st.session_state.lab.T2
                except ValueError:
                    T1 = None
                    T2 = None

                if T1 is not None:
                    Q1, st.session_state.I1 = pid_step(
                        st.session_state.SP1, T1, dt,
                        st.session_state.Kc1, st.session_state.Ki1, st.session_state.Kd1,
                        st.session_state.I1, st.session_state.prev_T1
                    )
                else:
                    Q1 = 0

                if T2 is not None:
                    Q2, st.session_state.I2 = pid_step(
                        st.session_state.SP2, T2, dt,
                        st.session_state.Kc2, st.session_state.Ki2, st.session_state.Kd2,
                        st.session_state.I2, st.session_state.prev_T2
                    )
                else:
                    Q2 = 0

                st.session_state.lab.Q1(Q1)
                st.session_state.lab.Q2(Q2)
                if hardware:
                    st.session_state.lab.LED(st.session_state.LED)

                if T1 is not None:
                    st.session_state.t.append(round(elapsed, 2))
                    st.session_state.T1.append(T1)
                    st.session_state.T2.append(T2)
                    st.session_state.Q1.append(Q1)
                    st.session_state.Q2.append(Q2)
                    st.session_state.SP1_log.append(st.session_state.SP1)
                    st.session_state.SP2_log.append(st.session_state.SP2)

                    st.session_state.prev_T1 = T1
                    st.session_state.prev_T2 = T2

            except Exception as e:
                st.error(f"Error: {e}")
                st.session_state.collecting = False
                close_lab()

# ------------------------------
# DOWNLOAD DATA WHEN STOPPED
# ------------------------------
if not st.session_state.collecting and len(st.session_state.t) > 0:
    df_out = pd.DataFrame(
        {
            "Time (s)": st.session_state.t,
            "SP1 (°C)": st.session_state.SP1_log,
            "T1 (°C)": st.session_state.T1,
            "Q1 (%)": st.session_state.Q1,
            "SP2 (°C)": st.session_state.SP2_log,
            "T2 (°C)": st.session_state.T2,
            "Q2 (%)": st.session_state.Q2,
        }
    )
    csv = df_out.to_csv(index=False)
    st.subheader("Download Data")
    st.download_button(
        "Download Data as CSV",
        data=csv,
        file_name="tclab_pid_data.csv",
        mime="text/csv",
    )

# ------------------------------
# AUTO REFRESH (AFTER RENDER)
# ------------------------------
if st.session_state.collecting:
    time.sleep(0.1)
    st.rerun()
