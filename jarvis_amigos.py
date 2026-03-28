import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Jarvis Final", page_icon="🤖")

# --- 2. SEGURIDAD ---
# PEGA AQUÍ LA LLAVE DEL PROYECTO NUEVO
API_KEY = "AIzaSyC8Q_7hBBV8_iiQVd_1kRkZjGeCz622UrM"
genai.configure(api_key=API_KEY)

# --- 3. DISEÑO ---
st.markdown("<h1 style='text-align: center; color: #0ff;'>🤖 Jarvis: Sistema Restaurado</h1>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. MODELO ---
try:
    # Usamos gemini-1.5-flash que es el más rápido para tu Samsung A36
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Error de inicio: {e}")

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. CHAT ---
if prompt := st.chat_input("Señor Jaider, ¿qué desea consultar?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Petición simple
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error técnico: {e}")
            st.info("Asegúrate de que la API Key sea la del PROYECTO NUEVO.")
