import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
import time
import glob
import paho.mqtt.client as paho
import json
from gtts import gTTS
from googletrans import Translator
import platform # Importado para mostrar la versión de Python

# --- CSS PESADILLA GÓTICA (Referencia Bloodborne: Azul Oscuro, Bronce, Tinta y Sangre) ---
base_css = """
<style>
/* ---------------------------------------------------- */
/* RESET Y FONDO AMBIENTAL */
/* ---------------------------------------------------- */
.stApp {
    /* Color de la noche de Yharnam o la Pesadilla: Azul/Negro muy oscuro. */
    background-color: #0F0F1A; 
    color: #C0C0C0; /* Texto de pergamino antiguo */
    font-family: 'Georgia', serif; 
}

/* ---------------------------------------------------- */
/* TIPOGRAFÍA Y ENCABEZADOS */
/* ---------------------------------------------------- */
h1 {
    /* Titular: Bronce envejecido o Oro oscuro */
    color: #9C7E4F; 
    text-align: center;
    /* Borde inferior como una reja forjada */
    border-bottom: 3px solid #4F4A5E; 
    padding-bottom: 10px;
    margin-bottom: 40px;
    font-size: 2.5em;
    letter-spacing: 3px;
    text-shadow: 1px 1px 5px #000000;
}

h3 {
    /* Subtítulos: Gris pizarra o plata mate */
    color: #A9A9A9; 
    margin-top: 25px;
    font-weight: normal;
    border-left: 4px solid #B22222; /* Acento Sangre */
    padding-left: 10px;
    font-size: 1.5em;
}

/* ---------------------------------------------------- */
/* BOTONES (Sello de Invocación) */
/* ---------------------------------------------------- */
.stButton>button {
    /* Acero oscuro, base de la Rueda de la Convocación */
    background-color: #383850; 
    /* Texto: Letras rúnicas en rojo sangre */
    color: #B22222; 
    /* Borde: Acento de metal forjado */
    border: 2px solid #9C7E4F; 
    padding: 10px 20px;
    font-weight: bold;
    border-radius: 10px;
    transition: all 0.3s;
    /* Sombra profunda */
    box-shadow: 0 6px #1A1A2A; 
    letter-spacing: 1px;
    width: 100%; /* Para que los botones se vean mejor */
}

.stButton>button:hover {
    background-color: #4F4F6A; 
    box-shadow: 0 10px #0F0F1A;
    transform: translateY(-3px);
}

.stButton>button:active {
    box-shadow: 0 3px #0F0F1A;
    transform: translateY(3px);
}

/* ---------------------------------------------------- */
/* SLIDER (El Dial de la Locura) */
/* ---------------------------------------------------- */
.stSlider .st-bd {
    /* Color de la barra inactiva */
    background-color: #4F4A5E; 
}
.stSlider .st-bv {
    /* Color de la barra activa */
    background-color: #B22222; 
}
.stSlider .st-bg {
    /* Color del pulgar (thumb) */
    background-color: #9C7E4F; 
    border: 2px solid #383850;
}


/* ---------------------------------------------------- */
/* MENSAJES DE ESTADO */
/* ---------------------------------------------------- */
.stSuccess, .stWarning, .stError {
    border-radius: 5px;
    padding: 10px;
}
.stSuccess {
    background-color: #1A2A1A; /* Verde oscuro místico */
    color: #A3D9A3;
    border-left: 4px solid #4CAF50;
}
.stError {
    background-color: #3A1A1A; /* Rojo oscuro de sangre */
    color: #FF6666;
    border-left: 4px solid #B22222;
}

</style>
"""
st.markdown(base_css, unsafe_allow_html=True)


# --- Variables y Funciones de MQTT ---

# Inicialización de estado
if 'analog_value' not in st.session_state:
    st.session_state.analog_value = 0.0

def on_publish(client,userdata,result): #create function for callback
    print("El Comando Arcano ha sido publicado. \n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received=str(message.payload.decode("utf-8"))
    st.markdown(f"**Recepción de la Efigie:** {message_received}")


# --- Configuración de Conexión ---
# Utilizando el broker IP provisto
broker="157.230.214.127"
port=1883
client1= paho.Client("GIT-HUB")
client1.on_message = on_message
# Conectar al cliente una sola vez al inicio para evitar re-conexiones en cada llamada
try:
    client1.connect(broker,port)
    st.info(f"Conectado al Nexo Cósmico: **{broker}:{port}**")
except Exception as e:
    st.error(f"Fallo al conectar al Nexo Cósmico: {e}")


# --- Interfaz Gótica (Control Manual de Runas) ---

st.title("🕯️ EL ALTAR DE CONEXIÓN: CONTROL MANUAL")
st.subheader("Rito de Control Remoto (Protocolo MQTT)")

# Muestra la versión de Python
st.markdown("---")
st.markdown(f"### 🐍 Oráculo de la Cuerda (Python):")
st.markdown(f"Versión de Python utilizada en el ritual: `{platform.python_version()}`")
st.markdown("---")


# --- Control Binario (ON/OFF) ---
st.markdown("### El Canto de las Runas Binarias (ON/OFF)")

# Contenedor para botones en dos columnas
col1, col2 = st.columns(2)

with col1:
    if st.button('INVOCAR LUZ (ON)', key='on_button'):
        act1="ON"
        try:
            message = json.dumps({"Act1": act1})
            ret= client1.publish("cmqtt_s", message)
            st.success("La Runa de la Luz (ON) ha sido grabada.")
        except Exception as e:
            st.error(f"Error al publicar el comando: {e}")

with col2:
    if st.button('DISIPAR SOMBRA (OFF)', key='off_button'):
        act1="OFF"
        try:
            message = json.dumps({"Act1": act1})
            ret= client1.publish("cmqtt_s", message)
            st.success("La Runa de la Sombra (OFF) ha sido grabada.")
        except Exception as e:
            st.error(f"Error al publicar el comando: {e}")

st.markdown("---")

# --- Control Analógico (SLIDER) ---
st.markdown("### El Dial de la Locura (Control Analógico)")

# Usamos el estado de sesión para mantener el valor del slider
st.session_state.analog_value = st.slider(
    'Selecciona el nivel de poder arcano (0.0 a 100.0):',
    0.0, 100.0, st.session_state.analog_value
)

st.markdown(f'**Nivel Arcano Seleccionado:** `{st.session_state.analog_value:.2f}`')

if st.button('GRABAR VALOR ANALÓGICO', key='analog_button'):
    try:
        # Publicación del valor analógico
        message = json.dumps({"Analog": float(st.session_state.analog_value)})
        ret= client1.publish("cmqtt_a", message)
        st.success(f"Valor Analógico ({st.session_state.analog_value:.2f}) transmitido al canal cósmico **'cmqtt_a'**.")
    except Exception as e:
        st.error(f"Error al grabar el valor analógico: {e}")





