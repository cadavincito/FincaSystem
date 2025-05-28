import streamlit as st
import paho.mqtt.client as mqtt
import json

# Configuración de la aplicación (DEBE SER EL PRIMER COMANDO DE STREAMLIT)
st.set_page_config(page_title="Sistema de Control de Finca", layout="wide")

# Inyectar CSS personalizado para centrar elementos
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
    /* Ajustar el ancho de los contenedores para mejor apariencia */
    .stTextInput > div, .stSlider > div, .stRadio > div {
        width: 50%;
        max-width: 500px;
        margin: auto;
    }
    .stButton > button {
        width: 100%;
        max-width: 500px;
        margin: auto;
    }
    /* Centrar los encabezados */
    h1, h2, h3 {
        text-align: center;
    }
    /* Ajustar el contenedor principal */
    .main .block-container {
        max-width: 800px;
        margin: 100px;
        padding: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Configuración de MQTT
broker = "broker.hivemq.com"  # Public MQTT broker
port = 1883
client_id = "Streamlit_FarmControl"
client = mqtt.Client(client_id)

# Variables para almacenar el estado (para feedback visual)
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
if "estado_puerta" not in st.session_state:
    st.session_state.estado_puerta = "Cerrada"

# Conectar al broker MQTT
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        st.success("Conectado al broker MQTT")
        # Suscribirse a topics de estado
        client.subscribe("farm/status/#")
    else:
        st.error("Error de conexión al broker MQTT")

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    if topic == "farm/status/fence":
        st.session_state.estado_cerca = "Encendida" if payload == "on" else "Apagada"
    elif topic == "farm/status/fence_power":
        st.session_state.potencia_cerca = int(payload)
    elif topic == "farm/status/ext_alarm":
        st.session_state.estado_alarma_ext = "Encendida" if payload == "on" else "Apagada"
    elif topic == "farm/status/int_alarm":
        st.session_state.estado_alarma_int = "Encendida" if payload == "on" else "Apagada"
    elif topic == "farm/status/light":
        st.session_state.estado_luz = "Encendida" if payload == "on" else "Apagada"
    elif topic == "farm/status/gate":
        st.session_state.estado_puerta = "Abierta" if payload == "open" else "Cerrada"

client.on_connect = on_connect
client.on_message = on_message
client.connect(broker, port)
client.loop_start()

# Barra lateral para navegación
pagina = st.sidebar.selectbox("Selecciona la Página de Control", ["Controles Externos", "Controles Internos"])

# Página de Controles Externos
if pagina == "Controles Externos":
    st.title("Controles Externos de la Finca")
    
    # Puerta Principal
    st.header("Puerta Principal")
    st.write(f"Estado actual: {st.session_state.estado_puerta}")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Abrir Puerta"):
            client.publish("farm/gate", "open")
            st.success("¡Puerta principal abierta!")
    with col2:
        if st.button("Cerrar Puerta"):
            client.publish("farm/gate", "close")
            st.success("¡Puerta principal cerrada!")
    
    # Cerca Eléctrica
    st.header("Cerca Eléctrica")
    st.write(f"Estado actual: {st.session_state.estado_cerca}, Potencia: {st.session_state.potencia_cerca}%")
    estado_cerca = st.radio("Estado de la Cerca", ["Encendida", "Apagada"], index=1 if st.session_state.estado_cerca == "Apagada" else 0)
    potencia_cerca = st.slider("Nivel de Potencia de la Cerca", 0, 100, st.session_state.potencia_cerca)
    if st.button("Aplicar Configuración de la Cerca"):
        accion = "on" if estado_cerca == "Encendida" else "off"
        client.publish("farm/fence", accion)
        client.publish("farm/fence_power", str(potencia_cerca))
        st.success(f"Cerca eléctrica {accion}, potencia ajustada a {potencia_cerca}%")
    
    # Alarma Externa
    st.header("Alarma Externa")
    st.write(f"Estado actual: {st.session_state.estado_alarma_ext}")
    col3, col4 = st.columns(2)
    with col3:
        if st.button("Activar Alarma Externa"):
            client.publish("farm/ext_alarm", "on")
            st.success("¡Alarma externa activada!")
    with col4:
        if st.button("Desactivar Alarma Externa"):
            client.publish("farm/ext_alarm", "off")
            st.success("¡Alarma externa desactivada!")
    
    # Simulación de Comando por Voz
    st.header("Comando por Voz (Simulación por Texto)")
    comando_voz = st.text_input("Ingresa el comando por voz (ej., 'abrir puerta', 'encender cerca')")
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
            st.error("Comando por voz desconocido")

# Página de Controles Internos
else:
    st.title("Controles Internos de la Finca")
    
    # Alarma Interna
    st.header("Alarma Interna")
    st.write(f"Estado actual: {st.session_state.estado_alarma_int}")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Activar Alarma Interna"):
            client.publish("farm/int_alarm", "on")
            st.success("¡Alarma interna activada!")
    with col2:
        if st.button("Desactivar Alarma Interna"):
            client.publish("farm/int_alarm", "off")
            st.success("¡Alarma interna desactivada!")
    
    # Luz de la Sala
    st.header("Luz de la Sala")
    st.write(f"Estado actual: {st.session_state.estado_luz}")
    col3, col4 = st.columns(2)
    with col3:
        if st.button("Encender Luz"):
            client.publish("farm/light", "on")
            st.success("¡Luz de la sala encendida!")
    with col4:
        if st.button("Apagar Luz"):
            client.publish("farm/light", "off")
            st.success("¡Luz de la sala apagada!")
    
    # Simulación de Comando por Voz
    st.header("Comando por Voz (Simulación por Texto)")
    comando_voz = st.text_input("Ingresa el comando por voz (ej., 'encender luz', 'activar alarma')")
    if st.button("Ejecutar Comando por Voz"):
        comando = comando_voz.lower()
        if comando == "activar alarma interna":
            client.publish("farm/int_alarm", "on")
            st.success("Comando por voz: ¡Alarma interna activada!")
        elif comando == "desactivar alarma interna":
            client.publish("farm/int_alarm", "off")
            st.success("Comando por voz: ¡Alarma interna desactivada!")
        elif comando == "encender luz":
            client.publish("farm/light", "on")
            st.success("Comando por voz: ¡Luz de la sala encendida!")
        elif comando == "apagar luz":
            client.publish("farm/light", "off")
            st.success("Comando por voz: ¡Luz de la sala apagada!")
        else:
            st.error("Comando por voz desconocido")

client.loop_stop()
