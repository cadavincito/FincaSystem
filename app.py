import streamlit as st
import paho.mqtt.publish as publish
import time

# Configuración de la aplicación
st.set_page_config(page_title="Sistema de Control de Finca", layout="wide")

# Configuración del broker MQTT
BROKER = "broker.hivemq.com"
TOPICOS = {
    "puerta_servo": "finca/puerta",
    "cerca_electrica": "finca/cerca",
    "alarma_externa": "finca/alarma_ext",
    "alarma_interna": "finca/alarma_int",
    "luz_sala": "finca/luz"
}

# Función para publicar por MQTT
def enviar_a_wokwi(dispositivo, accion, valor=None):
    topico = TOPICOS.get(dispositivo)
    if not topico:
        st.error("Dispositivo no reconocido")
        return
    mensaje = accion if valor is None else f"{accion}:{valor}"
    try:
        publish.single(topic=topico, payload=mensaje, hostname=BROKER)
        st.success(f"✅ Enviado a {dispositivo}: {mensaje}")
    except Exception as e:
        st.error(f"❌ Error al enviar mensaje: {e}")

# CSS personalizado para dark mode y centrar elementos
st.markdown("""
<style>
body, .main, .block-container {
    background-color: #121212;
    color: white;
}

h1, h2, h3, .stMarkdown, .stTextInput label, .stRadio label, .stSlider label, .stButton button {
    color: white;
}

.stButton, .stTextInput, .stSlider, .stRadio, .stMarkdown {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    margin: auto;
}
.stColumn {
    display: flex;
