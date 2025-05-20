import streamlit as st
import requests  # For simulated API calls to Wokwi

# Simulated API call to Wokwi (replace with actual Wokwi IoT communication)
def send_to_wokwi(device, action, value=None):
    # In a real setup, this would send HTTP requests to Wokwi's IoT API
    st.write(f"Simulated Wokwi action: {device} - {action} - {value if value else ''}")
    return {"status": "success"}

# Set up the Streamlit app with multi-page configuration
st.set_page_config(page_title="Farm Control System", layout="wide")

# Sidebar for navigation
page = st.sidebar.selectbox("Select Control Page", ["External Controls", "Internal Controls"])

# External Controls Page
if page == "External Controls":
    st.title("External Farm Controls")
    
    # Main Gate Control
    st.header("Main Gate")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Open Gate"):
            send_to_wokwi("gate_servo", "open")
            st.success("Main gate opened!")
    with col2:
        if st.button("Close Gate"):
            send_to_wokwi("gate_servo", "close")
            st.success("Main gate closed!")
    
    # Electric Fence Control
    st.header("Electric Fence")
    fence_status = st.radio("Fence Status", ["On", "Off"], index=1)
    fence_power = st.slider("Fence Power Level", 0, 100, 50)
    if st.button("Apply Fence Settings"):
        action = "on" if fence_status == "On" else "off"
        send_to_wokwi("electric_fence", action, fence_power)
        st.success(f"Electric fence {action}, power set to {fence_power}%")
    
    # External Alarm Control
    st.header("External Alarm")
    col3, col4 = st.columns(2)
    with col3:
        if st.button("Activate External Alarm"):
            send_to_wokwi("external_alarm", "on")
            st.success("External alarm activated!")
    with col4:
        if st.button("Deactivate External Alarm"):
            send_to_wokwi("external_alarm", "off")
            st.success("External alarm deactivated!")
    
    # Simulated Voice Command
    st.header("Voice Command (Text Simulation)")
    voice_command = st.text_input("Enter voice command (e.g., 'open gate', 'turn on fence')")
    if st.button("Execute Voice Command"):
        if voice_command.lower() == "open gate":
            send_to_wokwi("gate_servo", "open")
            st.success("Voice command: Main gate opened!")
        elif voice_command.lower() == "close gate":
            send_to_wokwi("gate_servo", "close")
            st.success("Voice command: Main gate closed!")
        elif voice_command.lower() == "turn on fence":
            send_to_wokwi("electric_fence", "on", 50)
            st.success("Voice command: Electric fence turned on!")
        elif voice_command.lower() == "turn off fence":
            send_to_wokwi("electric_fence", "off")
            st.success("Voice command: Electric fence turned off!")
        elif voice_command.lower() == "activate external alarm":
            send_to_wokwi("external_alarm", "on")
            st.success("Voice command: External alarm activated!")
        elif voice_command.lower() == "deactivate external alarm":
            send_to_wokwi("external_alarm", "off")
            st.success(" Pragmatic Solutions: Streamlit and Wokwi Code for Farm Control System

**Streamlit Code (app.py)**

```python
import streamlit as st
import requests

# Simulated Wokwi API call (replace with actual Wokwi IoT communication)
def send_to_wokwi(device, action, value=None):
    st.write(f"Wokwi action: {device} - {action} - {value if value else ''}")
    return {"status": "success"}

# App configuration
st.set_page_config(page_title="Farm Control System", layout="wide")

# Sidebar navigation
page = st.sidebar.selectbox("Select Control Page", ["External Controls", "Internal Controls"])

# External Controls Page
if page == "External Controls":
    st.title("External Farm Controls")
    
    # Main Gate
    st.header("Main Gate")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Open Gate"):
            send_to_wokwi("gate_servo", "open")
            st.success("Main gate opened!")
    with col2:
        if st.button("Close Gate"):
            send_to_wokwi("gate_servo", "close")
            st.success("Main gate closed!")
    
    # Electric Fence
    st.header("Electric Fence")
    fence_status = st.radio("Fence Status", ["On", "Off"], index=1)
    fence_power = st.slider("Fence Power Level", 0, 100, 50)
    if st.button("Apply Fence Settings"):
        action = "on" if fence_status == "On" else "off"
        send_to_wokwi("electric_fence", action, fence_power)
        st.success(f"Electric fence {action}, power set to {fence_power}%")
    
    # External Alarm
    st.header("External Alarm")
    col3, col4 = st.columns(2)
    with col3:
        if st.button("Activate External Alarm"):
            send_to_wokwi("external_alarm", "on")
            st.success("External alarm activated!")
    with col4:
        if st.button("Deactivate External Alarm"):
            send_to_wokwi("external_alarm", "off")
            st.success("External alarm deactivated!")
    
    # Voice Command Simulation
    st.header("Voice Command (Text Simulation)")
    voice_command = st.text_input("Enter voice command (e.g., 'open gate', 'turn on fence')")
    if st.button("Execute Voice Command"):
        command = voice_command.lower()
        if command == "open gate":
            send_to_wokwi("gate_servo", "open")
            st.success("Voice command: Main gate opened!")
        elif command == "close gate":
            send_to_wokwi("gate_servo", "close")
            st.success("Voice command: Main gate closed!")
        elif command == "turn on fence":
            send_to_wokwi("electric_fence", "on", 50)
            st.success("Voice command: Electric fence turned on!")
        elif command == "turn off fence":
            send_to_wokwi("electric_fence", "off")
            st.success("Voice command: Electric fence turned off!")
        elif command == "activate external alarm":
            send_to_wokwi("external_alarm", "on")
            st.success("Voice command: External alarm activated!")
        elif command == "deactivate external alarm":
            send_to_wokwi("external_alarm", "off")
            st.success("Voice command: External alarm deactivated!")
        else:
            st.error("Unknown voice command")

# Internal Controls Page
else:
    st.title("Internal Farm Controls")
    
    # Internal Alarm
    st.header("Internal Alarm")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Activate Internal Alarm"):
            send_to_wokwi("internal_alarm", "on")
            st.success("Internal alarm activated!")
    with col2:
        if st.button("Deactivate Internal Alarm"):
            send_to_wokwi("internal_alarm", "off")
            st.success("Internal alarm deactivated!")
    
    # Living Room Light
    st.header("Living Room Light")
    col3, col4 = st.columns(2)
    with col3:
        if st.button("Turn On Light"):
            send_to_wokwi("living_room_light", "on")
            st.success("Living room light turned on!")
    with col4:
        if st.button("Turn Off Light"):
            send_to_wokwi("living_room_light", "off")
            st.success("Living room light turned off!")
    
    # Voice Command Simulation
    st.header("Voice Command (Text Simulation)")
    voice_command = st.text_input("Enter voice command (e.g., 'turn on light', 'activate alarm')")
    if st.button("Execute Voice Command"):
        command = voice_command.lower()
        if command == "activate internal alarm":
            send_to_wokwi("internal_alarm", "on")
            st.success("Voice command: Internal alarm activated!")
        elif command == "deactivate internal alarm":
            send_to_wokwi("internal_alarm", "off")
            st.success("Voice command: Internal alarm deactivated!")
        elif command == "turn on light":
            send_to_wokwi("living_room_light", "on")
            st.success("Voice command: Living room light turned on!")
        elif command == "turn off light":
            send_to_wokwi("living_room_light", "off")
            st.success("Voice command: Living room light turned off!")
        else:
            st.error("Unknown voice command")
