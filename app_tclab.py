import streamlit as st
import pandas as pd
import numpy as np
import time
import tclab

# Check for hardware availability and set up TCLab
hardware = False

# Uncomment when running locally to use the TCLab
#tclab_hardware = st.checkbox("Use TCLab hardware", value=False)
#hardware = tclab_hardware.value

# Initialize session state variables for data persistence
if "collecting_data" not in st.session_state:
    st.session_state.collecting_data = False
    st.session_state.timestamps = []
    st.session_state.time = []
    st.session_state.T1_list = []
    st.session_state.T2_list = []
    st.session_state.Q1_list = []
    st.session_state.Q2_list = []

# Sidebar for controls to save space
st.sidebar.title("TCLab Controls")
Q1 = st.sidebar.slider("Heater 1 (%)", 0, 100, 0)
Q2 = st.sidebar.slider("Heater 2 (%)", 0, 100, 0)
if hardware:
    LED = st.sidebar.slider("LED Brightness (%)", 0, 100, 0)
    
# Add image under controls
url = "https://apmonitor.com/pdc/uploads/Main/tclab_transparent.png"
# In case URL isn't available
try:
    st.sidebar.image(url, caption="TCLab Device")
except:
    pass

# Create empty placeholder for the real-time line chart
combined_chart = st.empty()

# Start/Stop buttons
if st.button("Start Data Collection"):
    st.session_state.collecting_data = True
    st.session_state.timestamps = []
    st.session_state.time = []
    st.session_state.T1_list = []
    st.session_state.T2_list = []
    st.session_state.Q1_list = []
    st.session_state.Q2_list = []
    if hardware:
        TCLab = tclab.setup(connected=True)
    else:
        TCLab = tclab.setup(connected=False, speedup=10)
    st.session_state.lab = TCLab()
        
if st.button("Stop Data Collection"):
    st.session_state.collecting_data = False
    st.session_state.lab.close()
    
# Main loop for data collection
if st.session_state.collecting_data:
    with st.session_state.lab:
        # Start data collection loop
        for t in tclab.clock(600):  # Collect data for up to 600 seconds
            if not st.session_state.collecting_data:
                break  # Exit loop if Stop button is pressed

            # Read temperatures
            T1 = st.session_state.lab.T1
            T2 = st.session_state.lab.T2

            # Update data lists in session state
            if not st.session_state.time:
                st.session_state.time.append(0)
            else:
                st.session_state.time.append(st.session_state.time[-1]+1)
            st.session_state.timestamps.append(t)
            st.session_state.Q1_list.append(Q1)
            st.session_state.T1_list.append(T1)
            st.session_state.Q2_list.append(Q2)
            st.session_state.T2_list.append(T2)

            # Update heaters and LED based on slider values
            st.session_state.lab.Q1(Q1)
            st.session_state.lab.Q2(Q2)
            if hardware:
                st.session_state.lab.LED(LED)

            # Update DataFrame with new data
            data = pd.DataFrame({
                "Time": st.session_state.time,
                "Q1": st.session_state.Q1_list,
                "T1": st.session_state.T1_list,
                "Q2": st.session_state.Q2_list,
                "T2": st.session_state.T2_list
            })

            # Update real-time line chart with both temperature and heater data
            combined_chart.line_chart(data[["Q1", "T1", "Q2", "T2"]])

            # Small pause
            if not hardware:
                time.sleep(0.1)

# Convert data to DataFrame for downloading
if len(st.session_state.timestamps) > 0:
    data = pd.DataFrame({
        "Time (s)": np.arange(0,len(st.session_state.timestamps)),
        "Q1": st.session_state.Q1_list,
        "T1": st.session_state.T1_list,
        "Q2": st.session_state.Q2_list,
        "T2": st.session_state.T2_list
    })

    # Download button for the data
    csv = data.to_csv(index=False)
    st.download_button(
        label="Download Data as CSV",
        data=csv,
        file_name="tclab_data.csv",
        mime="text/csv"
    )
    st.session_state.collecting_data = False
else:
    st.write("No data collected yet.")
