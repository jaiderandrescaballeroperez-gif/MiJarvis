import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Jarvis - Jaider", page_icon="🤖")

# --- 2. SEGURIDAD ---
API_KEY = "AIzaSyBxGrdOa17_PCkLTiGElVJxZy3AWfZxNZY"
genai.configure(api_key=API_KEY)

# --- 3. DISEÑO ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #0ff; }
    h1 { text-align: center; text-shadow: 0 0 10px #0ff; }
    .stChatMessage { border: 1px solid #0ff; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>🤖 Jarvis Activo</h1>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. CONFIGURACIÓN DEL MODELO (EL TRUCO) ---
# Creamos una configuración que "salte" los errores de versión
generation_config = {
  "temperature": 0.7,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 65536,
}

try:
    # Usamos gemini-1.5-flash-latest que es la dirección más exacta
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash-latest",
        generation_config=generation_config,
    )
except Exception as e:
    st.error(f"Error inicial: {e}")

# Mostrar chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. INTERACCIÓN ---
if prompt := st.chat_input("Señor Jaider, ¿qué desea saber?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # LLAMADA DIRECTA AL CONTENIDO
            response = model.generate_content(prompt)
            
            if response and response.text:
                full_res = response.text
                st.markdown(full_res)
                st.session_state.messages.append({"role": "assistant", "content": full_res})
            else:
                st.error("Google no devolvió respuesta. Reintenta en 10 segundos.")
                
        except Exception as e:
            # Si falla el Flash, usamos el Pro como respaldo automático
            try:
                st.warning("Reintentando con modo de respaldo...")
                model_alt = genai.GenerativeModel("gemini-1.0-pro")
                response = model_alt.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except:
                st.error(f"Error de conexión de Google: {e}")

if st.sidebar.button("Limpiar"):
    st.session_state.messages = []
    st.rerun()
