import streamlit as st
import re 
from config.supabase_config import supabase_config 

st.markdown("<center><h1>Supabot: Supabase and Gemini AI</h1></center>", unsafe_allow_html=True)
_, col, _ = st.columns([3, 12, 3])

def validar_email(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email)

with col:
    with st.form("Register", clear_on_submit=True):
        st.header("Create Account")
        
        supabase = supabase_config()  # Obtenemos las claves de acceso y la url al proyecto
        
        user = st.text_input("User", placeholder="Digit your user", autocomplete="off")
        email = st.text_input("Email", placeholder="Digit your email", autocomplete="off")
        password = st.text_input("Password", placeholder="Digit your password", type="password")
        submit = st.form_submit_button("Register")
       
        if submit:
            if validar_email(email):
                try:
                    # Registro en auth
                    response = supabase.auth.sign_up({
                        "email": email,
                        "password": password
                    })

                    if response.user and response.user.id:
                        # Validar si ya está en la tabla usuarios
                        check = supabase.table("usuarios").select("id").eq("email", email).execute()

                        if check.data:
                            st.warning("Este correo ya fue registrado en la tabla 'usuarios'.")
                        else:
                            data = {"usuario": user, "email": email}
                            supabase.table("usuarios").insert(data).execute()
                            st.success("Usuario registrado exitosamente.")
                            st.switch_page("main.py")
                    else:
                        st.error("No se pudo completar el registro.")
                except Exception as e:
                    if "User already registered" in str(e):
                        st.warning("Este correo ya está registrado. Intenta iniciar sesión.")
                    else:
                        st.error(f"Error de acceso: {e}")
            else:
                st.warning("Write a valid email.")
