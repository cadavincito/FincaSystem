import streamlit as st
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

BROKER = "broker.hivemq.com"
TOPICOS = {
    "puerta_servo": "finca/puerta",
    "cerca_electrica": "finca/cerca",
    "alarma_externa": "finca/alarma_ext",
    "alarma_interna": "finca/alarma_int",
    "luz_sala": "finca/luz"
}

# Función para publicar mensajes
def enviar_a_wokwi(dispositivo, accion, valor=None):
    topico = TOPICOS.get(dispositivo)
    if not topico:
        st.error("Dispositivo no reconocido")
        return
    mensaje = accion if valor is None else f"{accion}:{valor}"
    publish.single(topic=topico, payload=mensaje, hostname=BROKER)
    st.success(f"✅ Enviado a {dispositivo}: {mensaje}")

# Mostrar estado MQTT
st.markdown("### ⏳ Esperando respuesta del ESP32...")

status_placeholder = st.empty()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.subscribe("finca/status")

def on_message(client, userdata, msg):
    if msg.topic == "finca/status":
        status_placeholder.success(f"✅ Mensaje del ESP32: {msg.payload.decode()}")

# Inicializar cliente MQTT solo una vez
if 'mqtt_initialized' not in st.session_state:
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, 1883, 60)
    client.loop_start()
    st.session_state['mqtt_initialized'] = True

# Interfaz Streamlit
pagina = st.sidebar.selectbox("Selecciona la Página de Control", ["Controles Externos", "Controles Internos"])

if pagina == "Controles Externos":
    st.title("Controles Externos de la Finca")

    st.header("Puerta Principal")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Abrir Puerta"):
            enviar_a_wokwi("puerta_servo", "abrir")
    with col2:
        if st.button("Cerrar Puerta"):
            enviar_a_wokwi("puerta_servo", "cerrar")

    st.header("Cerca Eléctrica")
    estado_cerca = st.radio("Estado de la Cerca", ["Encendida", "Apagada"], index=1)
    potencia_cerca = st.slider("Nivel de Potencia de la Cerca", 0, 100, 50)
    if st.button("Aplicar Configuración de la Cerca"):
        accion = "encender" if estado_cerca == "Encendida" else "apagar"
        enviar_a_wokwi("cerca_electrica", accion, potencia_cerca)

    st.header("Alarma Externa")
    col3, col4 = st.columns(2)
    with col3:
        if st.button("Activar Alarma Externa"):
            enviar_a_wokwi("alarma_externa", "encender")
    with col4:
        if st.button("Desactivar Alarma Externa"):
            enviar_a_wokwi("alarma_externa", "apagar")

elif pagina == "Controles Internos":
    st.title("Controles Internos de la Finca")

    st.header("Alarma Interna")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Activar Alarma Interna"):
            enviar_a_wokwi("alarma_interna", "encender")
    with col2:
        if st.button("Desactivar Alarma Interna"):
            enviar_a_wokwi("alarma_interna", "apagar")

    st.header("Luz de la Sala")
    col3, col4 = st.columns(2)
    with col3:
        if st.button("Encender Luz"):
            enviar_a_wokwi("luz_sala", "encender")
    with col4:
        if st.button("Apagar Luz"):
            enviar_a_wokwi("luz_sala", "apagar")
