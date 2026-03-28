import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Jarvis Final", page_icon="🤖")

# --- 2. SEGURIDAD (Modo Seguro) ---
# Intentamos obtener la llave desde los Secretos de Streamlit
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    # Si no hay secretos, usamos un cuadro de texto temporal para que la pegues
    api_key = st.sidebar.text_input("Pega tu nueva API Key aquí:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    # Probamos el modelo 1.0-pro que es el más estable ante advertencias
    model = genai.GenerativeModel('gemini-1.0-pro')
else:
    st.warning("Por favor, ingresa tu API Key en la barra lateral para comenzar.")
    st.stop()

# --- 3. DISEÑO ---
st.markdown("<h1 style='text-align: center; color: #0ff;'>🤖 Jarvis: Conexión Segura</h1>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. CHAT ---
if prompt := st.chat_input("Señor Jaider, el sistema está listo..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")
            st.info("Prueba con el modelo 'gemini-1.0-pro' si el flash sigue dando 404.")
