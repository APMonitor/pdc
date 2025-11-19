import streamlit as st
import pandas as pd
import numpy as np
import time
import threading
import tclab

# ---------------------------------
# Configuration
# ---------------------------------
hardware = False  # True for real device, False for emulator


# ---------------------------------
# Init Session State (main thread only)
# ---------------------------------
if "shared" not in st.session_state:
    st.session_state.shared = {
        "collecting": False,
        "Q1": 0,
        "Q2": 0,
        "LED": 0,
        "time_s": [],
        "T1": [],
        "T2": [],
        "Q1_hist": [],
        "Q2_hist": [],
        "LED_hist": [],
        "last_error": None,
    }

if "stop_event" not in st.session_state:
    st.session_state.stop_event = threading.Event()
if "lock" not in st.session_state:
    st.session_state.lock = threading.Lock()
if "worker" not in st.session_state:
    st.session_state.worker = None

shared = st.session_state.shared
lock = st.session_state.lock
stop_event = st.session_state.stop_event


# ---------------------------------
# Worker thread (NO streamlit calls here)
# ---------------------------------
def data_worker(shared_dict, stop_evt, lock_obj, use_hardware: bool):
    lab = None
    try:
        TCLab = tclab.setup(connected=use_hardware) if use_hardware else tclab.setup(
            connected=False, speedup=10
        )
        lab = TCLab()  # open serial/emulator

        t_index = 0
        while not stop_evt.is_set():
            # snapshot controls
            with lock_obj:
                q1 = int(shared_dict["Q1"])
                q2 = int(shared_dict["Q2"])
                led = int(shared_dict["LED"]) if use_hardware else 0

            # read sensors
            T1 = lab.T1
            T2 = lab.T2

            # write actuators
            lab.Q1(q1)
            lab.Q2(q2)
            if use_hardware:
                lab.LED(led)

            # store data
            with lock_obj:
                shared_dict["time_s"].append(t_index)
                shared_dict["T1"].append(T1)
                shared_dict["T2"].append(T2)
                shared_dict["Q1_hist"].append(q1)
                shared_dict["Q2_hist"].append(q2)
                shared_dict["LED_hist"].append(led)

            t_index += 1
            time.sleep(1.0 if use_hardware else 0.1)

    except Exception as e:
        # Record the error so the UI can display it
        with lock_obj:
            shared_dict["last_error"] = repr(e)
    finally:
        # Safe shutdown
        try:
            if lab is not None:
                try:
                    lab.Q1(0)
                    lab.Q2(0)
                    if use_hardware:
                        lab.LED(0)
                except Exception:
                    pass
                try:
                    lab.close()
                except Exception:
                    pass
        finally:
            with lock_obj:
                shared_dict["collecting"] = False
            stop_evt.clear()


# ---------------------------------
# Sidebar Controls
# ---------------------------------
st.sidebar.title("TCLab Controls")

# Sliders write into shared dict under lock
q1_val = st.sidebar.slider(
    "Heater 1 (%)", 0, 100, shared["Q1"], key="Q1_slider"
)
q2_val = st.sidebar.slider(
    "Heater 2 (%)", 0, 100, shared["Q2"], key="Q2_slider"
)
if hardware:
    led_val = st.sidebar.slider(
        "LED Brightness (%)", 0, 100, shared["LED"], key="LED_slider"
    )
else:
    led_val = 0

with lock:
    shared["Q1"] = q1_val
    shared["Q2"] = q2_val
    shared["LED"] = led_val

# Optional image
url = "https://apmonitor.com/pdc/uploads/Main/tclab_transparent.png"
try:
    st.sidebar.image(url, caption="TCLab Device")
except Exception:
    pass


# ---------------------------------
# Start / Stop Buttons
# ---------------------------------
col1, col2 = st.columns(2)
with col1:
    start_btn = st.button("Start Data Collection", disabled=shared["collecting"])
with col2:
    stop_btn = st.button("Stop Data Collection", disabled=not shared["collecting"])

if start_btn and not shared["collecting"]:
    # reset buffers
    with lock:
        shared["time_s"].clear()
        shared["T1"].clear()
        shared["T2"].clear()
        shared["Q1_hist"].clear()
        shared["Q2_hist"].clear()
        shared["LED_hist"].clear()
        shared["last_error"] = None
        shared["collecting"] = True

    stop_event.clear()

    # prevent multiple workers
    if st.session_state.worker is None or not st.session_state.worker.is_alive():
        st.session_state.worker = threading.Thread(
            target=data_worker,
            args=(shared, stop_event, lock, hardware),
            daemon=True,
        )
        st.session_state.worker.start()

if stop_btn and shared["collecting"]:
    stop_event.set()


# ---------------------------------
# Status + Debug info
# ---------------------------------
with lock:
    status = "Collecting" if shared["collecting"] else "Stopped"
    n_points = len(shared["time_s"])
    last_error = shared.get("last_error")

st.write(f"**Status:** {status}")
st.write(f"**Samples collected:** {n_points}")

if last_error:
    st.error(f"Worker error: {last_error}")


# ---------------------------------
# Plot
# ---------------------------------
combined_chart = st.empty()
with lock:
    if shared["time_s"]:
        df = pd.DataFrame(
            {
                "Time": shared["time_s"],
                "Q1": shared["Q1_hist"],
                "Q2": shared["Q2_hist"],
                "T1": shared["T1"],
                "T2": shared["T2"],
            }
        )
    else:
        df = None

if df is not None and not df.empty:
    combined_chart.line_chart(df[["Q1", "Q2", "T1", "T2"]])
else:
    st.write("No data collected yet.")


# ---------------------------------
# Download
# ---------------------------------
with lock:
    n = len(shared["time_s"])
    if n > 0:
        data = pd.DataFrame(
            {
                "Time (s)": np.arange(n, dtype=int),
                "Q1": shared["Q1_hist"],
                "T1": shared["T1"],
                "Q2": shared["Q2_hist"],
                "T2": shared["T2"],
            }
        )
    else:
        data = None

if data is not None and not data.empty:
    csv = data.to_csv(index=False)
    st.download_button(
        label="Download Data as CSV",
        data=csv,
        file_name="tclab_data.csv",
        mime="text/csv",
    )

# ---------------------------------
# Auto-refresh while collecting
# ---------------------------------
if shared["collecting"]:
    # Allow the worker to add a new point before rerendering
    time.sleep(1.0)
    st.rerun()
