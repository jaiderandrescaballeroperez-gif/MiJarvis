import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Jarvis Final", page_icon="🤖")

# --- 2. SEGURIDAD ---
# Usa la llave que creaste hoy (la que termina en xNZY)
API_KEY = "AIzaSyBxGrdOa17_PCkLTiGElVJxZy3AWfZxNZY"
genai.configure(api_key=API_KEY)

# --- 3. DISEÑO ---
st.markdown("<h1 style='text-align: center; color: #0ff;'>🤖 Jarvis: Modo Recuperación</h1>", unsafe_allow_html=True)

# --- 4. TRUCO MAESTRO: AUTO-DETECCIÓN ---
if "modelo_trabajo" not in st.session_state:
    try:
        # Le pedimos a Google la lista de lo que SÍ funciona para ti
        modelos = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        if modelos:
            # Seleccionamos el primero de la lista (el que Google prefiera)
            st.session_state.modelo_trabajo = modelos[0]
            st.success(f"Conectado exitosamente al núcleo: {modelos[0]}")
        else:
            st.session_state.modelo_trabajo = "models/gemini-1.5-flash"
    except Exception as e:
        st.session_state.modelo_trabajo = "models/gemini-1.5-flash"

model = genai.GenerativeModel(st.session_state.modelo_trabajo)

# --- 5. CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Señor Jaider, intentemos de nuevo..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error técnico: {e}")
            st.info("Si persiste, intenta crear una API Key en un PROYECTO NUEVO de Google Cloud.")
