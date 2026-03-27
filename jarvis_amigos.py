import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Jarvis - Jaider", page_icon="🤖", layout="wide")

# --- 2. SEGURIDAD (Nueva API Key) ---
NUEVA_API_KEY = "AIzaSyBxGrdOa17_PCkLTiGElVJxZy3AWfZxNZY"

# Configuración ultra-limpia
genai.configure(api_key=NUEVA_API_KEY)

# --- 3. ESTILO VISUAL ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #0ff; }
    h1 { text-align: center; text-shadow: 0 0 10px #0ff; }
    .stChatMessage { border: 1px solid #0ff; border-radius: 10px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>🤖 Jarvis: Sistema Activo</h1>", unsafe_allow_html=True)

# --- 4. INICIALIZAR MODELO ---
try:
    # Usamos el nombre del modelo sin prefijos raros
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Error al inicializar modelo: {e}")

# --- 5. GESTIÓN DE CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 6. INTERACCIÓN ---
if prompt := st.chat_input("¿Qué desea consultar, Señor Jaider?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Respuesta directa sin streaming para evitar errores 400/404
            response = model.generate_content(prompt)
            
            if response.text:
                full_res = response.text
                st.markdown(full_res)
                st.session_state.messages.append({"role": "assistant", "content": full_res})
            else:
                st.warning("El modelo no devolvió texto. Reintente.")
                
        except Exception as e:
            st.error(f"Detalle técnico: {e}")
            st.info("Nota: Si sale 404, espera 2 minutos a que Google active la nueva llave.")

# Botón para resetear
if st.sidebar.button("Borrar Memoria"):
    st.session_state.messages = []
    st.rerun()
