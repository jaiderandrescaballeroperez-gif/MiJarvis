import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Jarvis Final", page_icon="🤖")

# --- 2. SEGURIDAD ---
# PEGA AQUÍ LA LLAVE DEL PROYECTO NUEVO
NUEVA_API_KEY = "PEGA_AQUÍ_TU_NUEVA_LLAVE_DEL_PROYECTO_NUEVO"
genai.configure(api_key=NUEVA_API_KEY)

# --- 3. DISEÑO ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #0ff; }
    h1 { text-align: center; text-shadow: 0 0 10px #0ff; color: #0ff; }
    .stChatMessage { border: 1px solid #0ff; border-radius: 10px; background: rgba(0, 255, 255, 0.05); }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>🤖 Jarvis: Sistema Restaurado</h1>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. MOTOR DE RESPALDO ---
def generar_respuesta(prompt):
    # Lista de modelos por orden de estabilidad
    modelos_a_probar = ['gemini-1.5-flash', 'gemini-1.0-pro']
    
    for nombre in modelos_a_probar:
        try:
            model = genai.GenerativeModel(nombre)
            response = model.generate_content(prompt)
            if response.text:
                return response.text
        except:
            continue
    return "Error crítico: El servidor de Google sigue rechazando la conexión en este proyecto."

# Mostrar chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. INTERACCIÓN ---
if prompt := st.chat_input("Señor Jaider, ordene..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Buscando en la base de datos..."):
            respuesta = generar_respuesta(prompt)
            st.markdown(respuesta)
            st.session_state.messages.append({"role": "assistant", "content": respuesta})

if st.sidebar.button("Borrar"):
    st.session_state.messages = []
    st.rerun()
