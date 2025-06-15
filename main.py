import streamlit as st

# Debe ser la primera instrucción Streamlit
st.set_page_config("Supabot", layout="wide")

import re
from config.supabase_config import supabase_config
from streamlit_cookies_manager import CookieManager

# Inicialización de cookies
cookies = CookieManager()
if not cookies.ready():
    st.stop()

# Validar si ya hay una sesión activa
session = cookies.get("session")
if session:
    st.switch_page("pages/home.py")

# Encabezado de la app
st.markdown("<center><h1>Supabot: Supabase and Gemini AI</h1></center>", unsafe_allow_html=True)
_, col, _ = st.columns([3, 12, 3])

# Función para validar email
def validar_email(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email)

# Contenedor del formulario
with col:
    with st.container(border=True):
        st.header("Sign in")

        supabase = supabase_config()

        email = st.text_input("Email", placeholder="Digit your email", autocomplete="off")
        password = st.text_input("Password", placeholder="Digit your password", type="password")
        bt1, bt2 = st.columns([4, 1])
        submit = bt1.button("Enter", icon=":material/send:")

        if submit:
            if validar_email(email):
                try:
                    response = supabase.auth.sign_in_with_password({
                        "email": email,
                        "password": password
                    })

                    if response and response.user is not None:
                        # Guardar sesión en cookies
                        cookies["session"] = response.user.id
                        cookies.save()
                        st.success("Login exitoso. Redirigiendo...")
                        st.switch_page("pages/home.py")
                    else:
                        st.error("Credenciales inválidas o usuario no existe.")
                except Exception as e:
                    st.error(f"Error en autenticación: {str(e)}")
            else:
                st.warning("Write a valid email.")

        if bt2.button("CreateAccount", type="tertiary"):
            st.switch_page("pages/register.py")
