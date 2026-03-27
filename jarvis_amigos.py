import streamlit as st
import google.generativeai as genai
from google.generativeai.types import RequestOptions # <-- Esto es nuevo y clave
import os
import json
from datetime import datetime

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="¡Hola!", page_icon="🌐", layout="wide")

# --- 2. SEGURIDAD (Tu API Key) ---
GOOGLE_API_KEY = "AIzaSyD-JokRZd00OUzg1mMjpUGOLm9meRA1B8k"

# Configuración base
genai.configure(api_key=GOOGLE_API_KEY)

# --- 3. DISEÑO NEÓN ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at 50% -10%, #001a1a 0%, #000 100%) !important; }
    .stChatMessage { border-radius: 15px; border: 1px solid #0ff; background: rgba(0, 255, 255, 0.05) !important; }
    h1 { text-shadow: 0 0 15px #0ff; color: #0ff !important; text-align: center; font-family: 'Courier New', monospace; font-size: 3rem; }
    .stChatInput input { border-radius: 20px !important; border: 1px solid #0ff !important; }
    [data-testid="stSidebar"] { background-color: rgba(0, 0, 0, 0.8) !important; }
    </style>
    """, unsafe_allow_html=True)

HISTORIAL_DIR = "historial_chats"
if not os.path.exists(HISTORIAL_DIR):
    os.makedirs(HISTORIAL_DIR)

st.markdown("<h1>¡Hola!</h1>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 6. MODELO FORZANDO VERSIÓN V1 ---
try:
    # Usamos el modelo estándar
    model = genai.GenerativeModel('gemini-1.5-flash')
    # Forzamos a la librería a usar la versión 'v1' estable
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    ]
except Exception as e:
    st.error(f"Error al cargar el modelo: {e}")
    st.stop()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 7. INTERACCIÓN ---
if prompt := st.chat_input("¿En qué puedo ayudarlo, Señor Jaider?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        try:
            # AQUÍ ESTÁ EL TRUCO: Forzamos la versión v1 en la llamada
            response = model.generate_content(
                prompt,
                options=RequestOptions(api_version='v1') # <-- ESTO MATA EL ERROR 404
            )
            full_res = response.text
            placeholder.markdown(full_res)
            
        except Exception as e:
            st.error(f"Error detectado: {e}")
            full_res = "Señor, sigo teniendo problemas de conexión. Verifique la API Key o la versión."

    st.session_state.messages.append({"role": "assistant", "content": full_res})

    # GUARDAR HISTORIAL
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    archivo_ruta = os.path.join(HISTORIAL_DIR, f"chat_{timestamp}.json")
    with open(archivo_ruta, "w", encoding="utf-8") as f:
        json.dump(st.session_state.messages, f, ensure_ascii=False, indent=4)

with st.sidebar:
    st.write("📂 **Sesiones**")
    try:
        archivos = os.listdir(HISTORIAL_DIR)
        for arc in sorted(archivos, reverse=True)[:5]:
            st.caption(f"📄 {arc}")
    except:
        st.write("Sin historial.")
    
    if st.button("Limpiar Pantalla"):
        st.session_state.messages = []
        st.rerun()
