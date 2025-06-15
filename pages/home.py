import streamlit as st
from config.supabase_config import supabase_config
from streamlit_cookies_manager import CookieManager
import config.supabase_crud as sc
 #Inicialización de cookies
cookies = CookieManager()
if not cookies.ready():
    st.stop()

# Validar si ya hay una sesión activa
session = cookies.get("session")
if not session:
    st.switch_page("main.py")
    
supabase = supabase_config()

#Sidebar del home
st.subheader("Supabot")
with st.sidebar:
   if st.button("Logout", icon=":material/logout:", type="tertiary"):
        supabase.auth.sign_out()
        cookies.clear()
        cookies.save()
        st.switch_page("main.py")
   user = sc.getuser(session)    
   st.subheader(f":blue-background[Welcome {user}]")