import streamlit as st
import paho.mqtt.client as mqtt
import json

# Configuración de la aplicación (DEBE SER EL PRIMER COMANDO DE STREAMLIT)
st.set_page_config(page_title="Sistema de Control de Finca", layout="wide")

# Inyectar CSS personalizado para centrar elementos y mejorar la apariencia
st.markdown(
    """
    <style>
    /* Centrar contenedores de Streamlit */
    .stButton, .stTextInput, .stSlider, .stRadio, .stMarkdown {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        margin: auto;
    }
    /* Centrar columnas */
    .stColumn {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    /* Ajustar el ancho de los contenedores */
    .stTextInput > div, .stSlider > div, .stRadio > div {
        width: 50%;
        max-width: 500px;
        margin: auto;
    }
    .stButton > button {
        width: 100%;
        max-width: 500px;
        margin: auto;
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
    }
    /* Centrar los encabezados */
    h1, h2, h3 {
        text-align: center;
        color: #333;
    }
    /* Ajustar el contenedor principal */
    .main .block-container {
        max-width: 800px;
        margin: 20px auto;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    /* Estilo para estados */
    .status {
        font-size: 18px;
        font-weight: bold;
        color: #2e7d32;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Configuración de MQTT
broker = "broker.hivemq.com"
port = 1883
client_id = f"Streamlit_FarmControl_{int(time.time())}"  # ID único para evitar conflictos
client = mqtt.Client(client_id)

# Variables para almacenar el estado (para feedback visual)
if "estado_puerta" not in st.session_state:
    st.session_state.estado_puerta = "Cerrada"
if "estado_cerca" not in st.session_state:
    st.session_state.estado_cerca = "Apagada"
if "potencia_cerca" not in st.session_state:
    st.session_state.potencia_cerca = 50
if "estado_alarma_ext" not in st.session_state:
    st.session_state.estado_alarma_ext = "Apagada"
if "estado_alarma_int" not in st.session_state:
    st.session_state.estado_alarma_int = "Apagada"
if "estado_luz" not in st.session_state:
    st.session_state.estado_luz = "Apagada"

# Conectar al broker MQTT
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        st.success("Conectado al broker MQTT")
        client.subscribe("farm/status/#")
    else:
        st.error(f"Error de conexión al broker MQTT: {rc}")

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    print(f"Mensaje recibido en {topic}: {payload}")  # Depuración
    if topic == "farm/status/gate":
        st.session_state.estado_puerta = "Abierta" if payload == "open" else "Cerrada"
    elif topic == "farm/status/fence":
        st.session_state.estado_cerca = "Encendida" if payload == "on" else "Apagada"
    elif topic == "farm/status/fence_power":
        st.session_state.potencia_cerca = int(payload)
    elif topic == "farm/status/ext_alarm":
        st.session_state.estado_alarma_ext = "Encendida" if payload == "on" else "Apagada"
    elif topic == "farm/status/int_alarm":
        st.session_state.estado_alarma_int = "Encendida" if payload == "on" else "Apagada"
    elif topic == "farm/status/light":
        st.session_state.estado_luz = "Encendida" if payload == "on" else "Apagada"

client.on_connect = on_connect
client.on_message = on_message
client.connect(broker, port)
client.loop_start()

# Barra lateral para navegación
pagina = st.sidebar.selectbox("Selecciona la Página de Control", ["Controles Externos", "Controles Internos"])

# Página de Controles Externos
if pagina == "Controles Externos":
    st.title("Controles Externos de la Finca")
    
    # Puerta Principal (Servo)
    st.header("Puerta Principal")
    st.markdown(f"<p class='status'>Estado actual: {st.session_state.estado_puerta}</p>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Abrir Puerta"):
            client.publish("farm/gate", "open")
            st.success("¡Comando enviado: Puerta principal abierta!")
    with col2:
        if st.button("Cerrar Puerta"):
            client.publish("farm/gate", "close")
            st.success("¡Comando enviado: Puerta principal cerrada!")
    
    # Cerca Eléctrica (LED PWM)
    st.header("Cerca Eléctrica")
    st.markdown(f"<p class='status'>Estado actual: {st.session_state.estado_cerca}, Potencia: {st.session_state.potencia_cerca}%</p>", unsafe_allow_html=True)
    estado_cerca = st.radio("Estado de la Cerca", ["Encendida", "Apagada"], index=1 if st.session_state.estado_cerca == "Apagada" else 0)
    potencia_cerca = st.slider("Potencia de la Cerca", 0, 100, st.session_state.potencia_cerca)
    if st.button("Aplicar Configuración de la Cerca"):
        accion = "on" if estado_cerca == "Encendida" else "off"
        client.publish("farm/fence", accion)
        client.publish("farm/fence_power", str(potencia_cerca))
        st.success(f"¡Cerca eléctrica {accion}, potencia ajustada a {potencia_cerca}%!")
    
    # Alarma Externa (Buzzer)
    st.header("Alarma Externa")
    st.markdown(f"<p class='status'>Estado actual: {st.session_state.estado_alarma_ext}</p>", unsafe_allow_html=True)
    col3, col4 = st.columns(2)
    with col3:
        if st.button("Activar Alarma Externa"):
            client.publish("farm/ext_alarm", "on")
            st.success("¡Comando enviado: Alarma externa activada!")
    with col4:
        if st.button("Desactivar Alarma Externa"):
            client.publish("farm/ext_alarm", "off")
            st.success("¡Comando enviado: Alarma externa desactivada!")
    
    # Simulación de Comando por Voz
    st.header("Comando por Voz (Simulación por Texto)")
    comando_voz = st.text_input("Ingresa el comando por voz (ej., 'abrir puerta', 'encender cerca')", key="voz_externa")
    if st.button("Ejecutar Comando por Voz"):
        comando = comando_voz.lower()
        if comando == "abrir puerta":
            client.publish("farm/gate", "open")
            st.success("Comando por voz: ¡Puerta principal abierta!")
        elif comando == "cerrar puerta":
            client.publish("farm/gate", "close")
            st.success("Comando por voz: ¡Puerta principal cerrada!")
        elif comando == "encender cerca":
            client.publish("farm/fence", "on")
            st.success("Comando por voz: ¡Cerca eléctrica encendida!")
        elif comando == "apagar cerca":
            client.publish("farm/fence", "off")
            st.success("Comando por voz: ¡Cerca eléctrica apagada!")
        elif comando == "activar alarma externa":
            client.publish("farm/ext_alarm", "on")
            st.success("Comando por voz: ¡Alarma externa activada!")
        elif comando == "desactivar alarma externa":
            client.publish("farm/ext_alarm", "off")
            st.success("Comando por voz: ¡Alarma externa desactivada!")
        else:
            st.error("Comando por voz no reconocido. Prueba con 'abrir puerta', 'cerrar puerta', 'encender cerca', etc.")

# Página de Controles Internos
else:
    st.title("Controles Internos de la Finca")
    
    # Alarma Interna (Buzzer)
    st.header("Alarma Interna")
    st.markdown(f"<p class='status'>Estado actual: {st.session_state.estado_alarma_int}</p>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Activar Alarma Interna"):
            client.publish("farm/int_alarm", "on")
            st.success("¡Comando enviado: Alarma interna activada!")
    with col2:
        if st.button("Desactivar Alarma Interna"):
            client.publish("farm/int_alarm", "off")
            st.success("¡Comando enviado: Alarma interna desactivada!")
    
    # Luz de la Sala (LED)
    st.header("Luz de la Sala")
    st.markdown(f"<p class='status'>Estado actual: {st.session_state.estado_luz}</p>", unsafe_allow_html
