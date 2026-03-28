import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Jarvis Final", page_icon="🤖")

# --- 2. SEGURIDAD ---
# Intentamos usar Secrets (Recomendado), si no, usa la llave directa
if "GOOGLE_API_KEY" in st.secrets:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
else:
    API_KEY = "AIzaSyC8Q_7hBBV8_iiQVd_1kRkZjGeCz622UrM"

genai.configure(api_key=API_KEY)

# --- 3. DISEÑO ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #0ff; }
    h1 { text-align: center; text-shadow: 0 0 10px #0ff; }
    .stChatMessage { border: 1px solid #0ff; border-radius: 10px; background: rgba(0,255,255,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>🤖 Jarvis: Conexión Estable</h1>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. MODELO ---
try:
    # Usamos gemini-1.5-flash-latest para asegurar la versión más compatible
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    st.error(f"Error de inicio: {e}")

# Mostrar mensajes previos
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. CHAT ---
if prompt := st.chat_input("Señor Jaider, el sistema está en línea..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            if response.text:
                full_res = response.text
                st.markdown(full_res)
                st.session_state.messages.append({"role": "assistant", "content": full_res})
        except Exception as e:
            st.error(f"Error técnico: {e}")
            st.info("Si sale 404, es posible que la llave nueva aún se esté activando. Espera 2 minutos.")
