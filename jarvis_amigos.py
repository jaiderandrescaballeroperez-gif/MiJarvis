import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Jarvis Final", page_icon="🤖")

# --- 2. SEGURIDAD (Modo Invisible) ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ Falta la llave en los Secrets de Streamlit.")
    st.stop()

# --- 3. DISEÑO VISUAL ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #0ff; }
    h1 { text-align: center; text-shadow: 0 0 10px #0ff; }
    .stChatMessage { border: 1px solid #0ff; border-radius: 10px; background: rgba(0,255,255,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>🤖 Jarvis: Protocolo Activo</h1>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. MOTOR DE IA ---
model = genai.GenerativeModel('gemini-1.5-flash')

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. INTERACCIÓN ---
if prompt := st.chat_input("Señor Jaider, sistema listo para su consulta..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Petición directa al modelo
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error técnico: {e}")
