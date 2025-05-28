import streamlit as st
import requests

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

    .stButton > button{
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

# Función simulada para comunicación con Wokwi
def enviar_a_wokwi(dispositivo, accion, valor=None):
    st.write(f"Acción simulada en Wokwi: {dispositivo} - {accion} - {valor if valor else ''}")
    return {"estado": "éxito"}

# Barra lateral para navegación
pagina = st.sidebar.selectbox("Selecciona la Página de Control", ["Controles Externos", "Controles Internos"])

# Página de Controles Externos
if pagina == "Controles Externos":
    st.title("Controles Externos de la Finca")
    
    # Puerta Principal
    st.header("Puerta Principal")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Abrir Puerta"):
            enviar_a_wokwi("puerta_servo", "abrir")
            st.success("¡Puerta principal abierta!")
    with col2:
        if st.button("Cerrar Puerta"):
            enviar_a_wokwi("puerta_servo", "cerrar")
            st.success("¡Puerta principal cerrada!")
    
    # Cerca Eléctrica
    st.header("Cerca Eléctrica")
    estado_cerca = st.radio("Estado de la Cerca", ["Encendida", "Apagada"], index=1)
    potencia_cerca = st.slider("Nivel de Potencia de la Cerca", 0, 100, 50)
    if st.button("Aplicar Configuración de la Cerca"):
        accion = "encender" if estado_cerca == "Encendida" else "apagar"
        enviar_a_wokwi("cerca_electrica", accion, potencia_cerca)
        st.success(f"Cerca eléctrica {accion}, potencia ajustada a {potencia_cerca}%")
    
    # Alarma Externa
    st.header("Alarma Externa")
    col3, col4 = st.columns(2)
    with col3:
        if st.button("Activar Alarma Externa"):
            enviar_a_wokwi("alarma_externa", "encender")
            st.success("¡Alarma externa activada!")
    with col4:
        if st.button("Desactivar Alarma Externa"):
            enviar_a_wokwi("alarma_externa", "apagar")
            st.success("¡Alarma externa desactivada!")
    
    # Simulación de Comando por Voz
    st.header("Comando por Voz (Simulación por Texto)")
    comando_voz = st.text_input("Ingresa el comando por voz (ej., 'abrir puerta', 'encender cerca')")
    if st.button("Ejecutar Comando por Voz"):
        comando = comando_voz.lower()
        if comando == "abrir puerta":
            enviar_a_wokwi("puerta_servo", "abrir")
            st.success("Comando por voz: ¡Puerta principal abierta!")
        elif comando == "cerrar puerta":
            enviar_a_wokwi("puerta_servo", "cerrar")
            st.success("Comando por voz: ¡Puerta principal cerrada!")
        elif comando == "encender cerca":
            enviar_a_wokwi("cerca_electrica", "encender", 50)
            st.success("Comando por voz: ¡Cerca eléctrica encendida!")
        elif comando == "apagar cerca":
            enviar_a_wokwi("cerca_electrica", "apagar")
            st.success("Comando por voz: ¡Cerca eléctrica apagada!")
        elif comando == "activar alarma externa":
            enviar_a_wokwi("alarma_externa", "encender")
            st.success("Comando por voz: ¡Alarma externa activada!")
        elif comando == "desactivar alarma externa":
            enviar_a_wokwi("alarma_externa", "apagar")
            st.success("Comando por voz: ¡Alarma externa desactivada!")
        else:
            st.error("Comando por voz desconocido")

# Página de Controles Internos
else:
    st.title("Controles Internos de la Finca")
    
    # Alarma Interna
    st.header("Alarma Interna")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Activar Alarma Interna"):
            enviar_a_wokwi("alarma_interna", "encender")
            st.success("¡Alarma interna activada!")
    with col2:
        if st.button("Desactivar Alarma Interna"):
            enviar_a_wokwi("alarma_interna", "apagar")
            st.success("¡Alarma interna desactivada!")
    
    # Luz de la Sala
    st.header("Luz de la Sala")
    col3, col4 = st.columns(2)
    with col3:
        if st.button("Encender Luz"):
            enviar_a_wokwi("luz_sala", "encender")
            st.success("¡Luz de la sala encendida!")
    with col4:
        if st.button("Apagar Luz"):
            enviar_a_wokwi("luz_sala", "apagar")
            st.success("¡Luz de la sala apagada!")
    
    # Simulación de Comando por Voz
    st.header("Comando por Voz (Simulación por Texto)")
    comando_voz = st.text_input("Ingresa el comando por voz (ej., 'encender luz', 'activar alarma')")
    if st.button("Ejecutar Comando por Voz"):
        comando = comando_voz.lower()
        if comando == "activar alarma interna":
            enviar_a_wokwi("alarma_interna", "encender")
            st.success("Comando por voz: ¡Alarma interna activada!")
        elif comando == "desactivar alarma interna":
            enviar_a_wokwi("alarma_interna", "apagar")
            st.success("Comando por voz: ¡Alarma interna desactivada!")
        elif comando == "encender luz":
            enviar_a_wokwi("luz_sala", "encender")
            st.success("Comando por voz: ¡Luz de la sala encendida!")
        elif comando == "apagar luz":
            enviar_a_wokwi("luz_sala", "apagar")
            st.success("Comando por voz: ¡Luz de la sala apagada!")
        else:
            st.error("Comando por voz desconocido")
