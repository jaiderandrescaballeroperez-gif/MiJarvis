import streamlit as st
import google.generativeai as genai
import os
import json
from datetime import datetime

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="¡Hola!", page_icon="🌐", layout="wide")

# --- 2. SEGURIDAD ---
GOOGLE_API_KEY = "AIzaSyD-JokRZd00OUzg1mMjpUGOLm9meRA1B8k"
genai.configure(api_key=GOOGLE_API_KEY)

# --- 3. DISEÑO NEÓN ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at 50% -10%, #001a1a 0%, #000 100%) !important; }
    .stChatMessage { border-radius: 15px; border: 1px solid #0ff; background: rgba(0, 255, 255, 0.05) !important; }
    h1 { text-shadow: 0 0 15px #0ff; color: #0ff !important; text-align: center; font-family: 'Courier New', monospace; font-size: 3rem; }
    .stChatInput input { border-radius: 20px !important; border: 1px solid #0ff !important; }
    </style>
    """, unsafe_allow_html=True)

HISTORIAL_DIR = "historial_chats"
if not os.path.exists(HISTORIAL_DIR):
    os.makedirs(HISTORIAL_DIR)

st.markdown("<h1>¡Hola!</h1>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 6. MODELO CON NOMBRE ALTERNATIVO ---
try:
    # Cambia 'gemini-1.5-flash' por este nombre más específico:
    model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
except Exception as e:
    st.error(f"Error al cargar el modelo: {e}")
    st.stop()

# --- 7. CHAT ---
if prompt := st.chat_input("¿En qué puedo ayudarlo, Señor Jaider?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        try:
            # Enviar mensaje directo para evitar errores de historial
            response = model.generate_content(prompt)
            full_res = response.text
            placeholder.markdown(full_res)
            
        except Exception as e:
            st.error(f"Error: {e}")
            full_res = "Hubo un error de conexión."

    st.session_state.messages.append({"role": "assistant", "content": full_res})

    # GUARDAR
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    with open(os.path.join(HISTORIAL_DIR, f"chat_{timestamp}.json"), "w", encoding="utf-8") as f:
        json.dump(st.session_state.messages, f, ensure_ascii=False, indent=4)

with st.sidebar:
    st.write("📂 **Historial**")
    archivos = os.listdir(HISTORIAL_DIR)
    for arc in sorted(archivos, reverse=True)[:5]:
        st.caption(f"📄 {arc}")
    if st.button("Limpiar Pantalla"):
        st.session_state.messages = []
        st.rerun()
