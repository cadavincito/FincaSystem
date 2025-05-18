import streamlit as st
import paho.mqtt.client as mqtt
import speech_recognition as sr
from PIL import Image

# Configuración MQTT
#def on_connect(client, userdata, flags, rc):
   # client.subscribe("casa/proximidad")

#client = mqtt.Client()
#client.on_connect = on_connect
#client.connect("broker.hivemq.com", 1883, 60)
#client.loop_start()

# Estado de dispositivos
if "cerca" not in st.session_state:
    st.session_state.cerca = "OFF"
    st.session_state.puerta = "CLOSED"
    st.session_state.alarma = "OFF"
    st.session_state.luces = "OFF"

# Navegación
st.sidebar.title("Sistema de Seguridad")
page = st.sidebar.selectbox("Selecciona una página", ["Control Interior", "Control Perímetro"])

if page == "Control Interior":
    st.title("Control Interior")
    if st.button("Escuchar comando de voz"):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.write("Habla...")
            audio = recognizer.listen(source)
            try:
                comando = recognizer.recognize_google(audio, language="es-ES").lower()
                st.write(f"Comando: {comando}")
                if "puerta" in comando:
                    st.session_state.puerta = "OPEN" if "abrir" in comando else "CLOSED"
                    client.publish("casa/puerta", st.session_state.puerta)
                if "alarma" in comando:
                    st.session_state.alarma = "ON" if "encender" in comando else "OFF"
                    client.publish("casa/alarma", st.session_state.alarma)
            except sr.UnknownValueError:
                st.write("No se entendió el comando")
    col1, col2 = st.columns(2)
    with col1:
        st.image("puerta_abierta.png" if st.session_state.puerta == "OPEN" else "puerta_cerrada.png", caption="Puerta")
        if st.button("Abrir/Cerrar Puerta", key="puerta"):
            st.session_state.puerta = "OPEN" if st.session_state.puerta == "CLOSED" else "CLOSED"
            client.publish("casa/puerta", st.session_state.puerta)
    with col2:
        st.image("alarma_on.png" if st.session_state.alarma == "ON" else "alarma_off.png", caption="Alarma")
        if st.button("Activar/Desactivar Alarma", key="alarma"):
            st.session_state.alarma = "ON" if st.session_state.alarma == "OFF" else "OFF"
            client.publish("casa/alarma", st.session_state.alarma)

elif page == "Control Perímetro":
    st.title("Control Perímetro")
    col1, col2 = st.columns(2)
    with col1:
        cerca_state = st.checkbox("Cerca Eléctrica", value=st.session_state.cerca == "ON", key="cerca")
        st.image("cerca_on.png" if cerca_state else "cerca_off.png", caption="Cerca")
        if cerca_state != (st.session_state.cerca == "ON"):
            st.session_state.cerca = "ON" if cerca_state else "OFF"
            client.publish("casa/cerca", st.session_state.cerca)
    with col2:
        luces_state = st.checkbox("Luces Perímetro", value=st.session_state.luces == "ON", key="luces")
        st.image("luces_on.png" if luces_state else "luces_off.png", caption="Luces")
        if luces_state != (st.session_state.luces == "ON"):
            st.session_state.luces = "ON" if luces_state else "OFF"
            client.publish("casa/luces", st.session_state.luces)
