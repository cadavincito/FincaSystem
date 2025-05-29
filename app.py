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

# Funcín para publicar por MQTT
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

# CSS personalizado para centrar elementos
st.markdown("""
<style>
.stButton, .stTextInput, .stSlider, .stRadio, .stMarkdown {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    margin: auto;
}
.stColumn {
    display: flex;
    justify-content: center;
    align-items: center;
}
.stTextInput > div, .stSlider > div, .stRadio > div {
    width: 50%;
    max-width: 500px;
    margin: auto;
}
.stButton > button{
    width: 100%;
    max-width: 500px;
    margin: auto;
}
h1, h2, h3 {
    text-align: center;
}
.main .block-container {
    max-width: 800px;
    margin: 100px auto;
    padding: 20px;
}
</style>
""", unsafe_allow_html=True)

# Mensaje de estado
st.info("⏳ Esperando respuesta del ESP32... Asegúrate de que esté encendido y conectado al mismo broker MQTT")

# Selector lateral
pagina = st.sidebar.selectbox("Selecciona la Página de Control", ["Controles Externos", "Controles Internos"])

# CONTROLES EXTERNOS
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

    st.header("Comando por Voz (Texto Simulado)")
    comando_voz = st.text_input("Ejemplo: abrir puerta, encender cerca, etc.")
    if st.button("Ejecutar Comando por Voz"):
        comando = comando_voz.lower()
        if comando == "abrir puerta":
            enviar_a_wokwi("puerta_servo", "abrir")
        elif comando == "cerrar puerta":
            enviar_a_wokwi("puerta_servo", "cerrar")
        elif comando == "encender cerca":
            enviar_a_wokwi("cerca_electrica", "encender", 50)
        elif comando == "apagar cerca":
            enviar_a_wokwi("cerca_electrica", "apagar")
        elif comando == "activar alarma externa":
            enviar_a_wokwi("alarma_externa", "encender")
        elif comando == "desactivar alarma externa":
            enviar_a_wokwi("alarma_externa", "apagar")
        else:
            st.error("Comando por voz desconocido")

# CONTROLES INTERNOS
else:
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

    st.header("Comando por Voz (Texto Simulado)")
    comando_voz = st.text_input("Ejemplo: encender luz, activar alarma interna, etc.")
    if st.button("Ejecutar Comando por Voz"):
        comando = comando_voz.lower()
        if comando == "activar alarma interna":
            enviar_a_wokwi("alarma_interna", "encender")
        elif comando == "desactivar alarma interna":
            enviar_a_wokwi("alarma_interna", "apagar")
        elif comando == "encender luz":
            enviar_a_wokwi("luz_sala", "encender")
        elif comando == "apagar luz":
            enviar_a_wokwi("luz_sala", "apagar")
        else:
            st.error("Comando por voz desconocido")
