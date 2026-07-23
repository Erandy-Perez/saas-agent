import warnings
# Silenciar las advertencias de Google y Python en la terminal
warnings.filterwarnings("ignore")

import streamlit as st
from agente import inicializar_motor
import time

# Configuración
st.set_page_config(page_title="ApexCore", layout="centered")

def cargar_css(archivo_css):
    try:
        with open(archivo_css) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

cargar_css("frontend/style.css")

@st.cache_resource(show_spinner=False)
def cargar_agente():
    return inicializar_motor()

try:
    motor_rag, motor_optimizacion = cargar_agente()
except Exception as e:
    st.error(f"Error de sistema: {e}")
    st.stop()

# Títulos
st.markdown("<h1>ApexCore</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Asistente de Ingeniería y Arquitectura</div>", unsafe_allow_html=True)

query_ejemplo = None

# Botones con breves descripciones
st.write("")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Endpoint ETL"):
        query_ejemplo = "¿Cuál es el endpoint exacto y el método HTTP para ejecutar un proceso ETL?"
    st.caption("Ver la ruta y método de la API.")

with col2:
    if st.button("Recuperar API Key"):
        query_ejemplo = "¿Cómo puedo regenerar mi API Key desde el Panel de Control si fue comprometida?"
    st.caption("Pasos en caso de filtración.")

with col3:
    if st.button("Planes y Costos"):
        query_ejemplo = "¿Cuántas llamadas API incluye el Plan Professional y cuál es su costo?"
    st.caption("Precios y límites de uso.")

st.write("")

# Formulario (Arreglando el error del label)
with st.form(key="busqueda_form", clear_on_submit=True):
    # Se le da un nombre ("Consulta"), pero se oculta ("collapsed") para que no estorbe ni marque error
    input_usuario = st.text_input(
        label="Consulta", 
        label_visibility="collapsed", 
        placeholder="Ingresa tu consulta técnica aquí..."
    )
    
    # Centrar el botón de enviar usando columnas vacías a los lados
    _, col_btn, _ = st.columns([2, 1, 2])
    with col_btn:
        submit = st.form_submit_button("Enviar") 

consulta_final = query_ejemplo if query_ejemplo else (input_usuario if submit else None)

if consulta_final:
    with st.spinner("Analizando arquitectura y base de conocimiento..."):
        time.sleep(0.5) 
        resultado = motor_rag.invoke(consulta_final)
        
        st.write("")
        # Adiós st.info (azul). Usamos un div oscuro y elegante
        st.markdown(f"<div class='respuesta-cristal'>{resultado}</div>", unsafe_allow_html=True)

        with st.expander("Metadatos de Búsqueda (Multi-Query)"):
            st.write(motor_optimizacion.invoke({"question": consulta_final}))
