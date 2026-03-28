import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Jarvis Final", page_icon="🤖")

# --- 2. SEGURIDAD ---
# ASEGÚRATE DE QUE ESTA SEA LA LLAVE DEL PROYECTO NUEVO QUE CREASTE
API_KEY = "AIzaSyC8Q_7hBBV8_iiQVd_1kRkZjGeCz622UrM"
genai.configure(api_key=API_KEY)

# --- 3. DISEÑO ---
st.markdown("<h1 style='text-align: center; color: #0ff;'>🤖 Jarvis Online</h1>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. FUNCIÓN DE RESPUESTA RÁPIDA ---
def chat_con_google(query):
    try:
        # Usamos el modelo más básico para asegurar conexión
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(query)
        return response.text
    except Exception as e:
        return f"Error de conexión: {str(e)}"

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. INTERACCIÓN ---
if prompt := st.chat_input("Escriba aquí, Señor Jaider..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Esto evita que se quede cargando infinito
        with st.status("Conectando...", expanded=True) as status:
            respuesta = chat_con_google(prompt)
            status.update(label="Respuesta recibida", state="complete", expanded=False)
            
        st.markdown(respuesta)
        st.session_state.messages.append({"role": "assistant", "content": respuesta})

if st.sidebar.button("Limpiar"):
    st.session_state.messages = []
    st.rerun()
