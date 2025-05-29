import streamlit as st
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import threading

# Configuración general
st.set_page_config(page_title="Sistema de Control de Finca", layout="wide")
BROKER = "broker.hivemq.com"
TOPICOS = {
    "puerta_servo": "finca/puerta",
    "cerca_electrica": "finca/cerca",
    "alarma_externa": "finca/alarma_ext",
    "alarma_interna": "finca/alarma_int",
    "luz_sala": "finca/luz"
}
TOPICO_STATUS = "finca/status"
estado_esp32 = st.empty()

# Función para publicar
def enviar_a_wokwi(dispositivo, accion, valor=None):
    topico = TOPICOS.get(dispositivo)
    if not topico:
        st.error("Dispositivo no reconocido")
        return
    mensaje = accion if valor is None else f"{accion}:{valor}"
    publish.single(topic=topico, payload=mensaje, hostname=BROKER)
    st.success(f"Enviado a {dispositivo}: {mensaje}")

# Función para manejar mensajes entrantes del ESP32
def on_message(client, userdata, msg):
    if msg.topic == TOPICO_STATUS:
        mensaje = msg.payload.decode()
        estado_esp32.info(f"✅ ESP32 responde: {mensaje}")

# Hilo MQTT para escuchar respuestas del ESP32
def iniciar_mqtt_sub():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(BROKER, 1883, 60)
    client.subscribe(TOPICO_STATUS)
    client.loop_forever()

# Iniciar suscripción MQTT en segundo plano
if "mqtt_thread_started" not in st.session_state:
    thread = threading.Thread(target=iniciar_mqtt_sub, daemon=True)
    thread.start()
    st.session_state["mqtt_thread_started"] = True
    estado_esp32.warning("⏳ Esperando respuesta del ESP32...")

# UI de control (simplificado para ejemplo)
st.title("Controles de Finca")
if st.button("Abrir Puerta"):
    enviar_a_wokwi("puerta_servo", "abrir")
