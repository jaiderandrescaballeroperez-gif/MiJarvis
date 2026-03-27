import streamlit as st
import requests
import json

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Jarvis Ultra", page_icon="🤖")

# --- 2. SEGURIDAD ---
API_KEY = "AIzaSyBxGrdOa17_PCkLTiGElVJxZy3AWfZxNZY"
# Construimos la URL manual para forzar la versión estable v1
URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"

# --- 3. DISEÑO ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ffff; }
    .stChatMessage { border: 1px solid #00ffff; border-radius: 15px; background: rgba(0, 255, 255, 0.05); }
    h1 { text-align: center; text-shadow: 0 0 15px #0ff; font-family: 'Courier New', monospace; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>🤖 JARVIS: PROTOCOLO DIRECTO</h1>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. FUNCIÓN DE ENVÍO DIRECTO ---
def llamar_ai(texto):
    payload = {
        "contents": [{"parts": [{"text": texto}]}]
    }
    headers = {'Content-Type': 'application/json'}
    
    # Hacemos la petición manual al servidor de Google
    response = requests.post(URL, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 200:
        datos = response.json()
        return datos['candidates'][0]['content']['parts'][0]['text']
    else:
        return f"Error de servidor ({response.status_code}): {response.text}"

# --- 5. INTERACCIÓN ---
if prompt := st.chat_input("Señor Jaider, ordene..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Conectando con el núcleo..."):
            respuesta = llamar_ai(prompt)
            st.markdown(respuesta)
            st.session_state.messages.append({"role": "assistant", "content": respuesta})

if st.sidebar.button("Reiniciar Sistema"):
    st.session_state.messages = []
    st.rerun()
