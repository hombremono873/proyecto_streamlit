from config.supabase_config import supabase_config

supabase = supabase_config()

def getuser(user_id):
    response = supabase.table("usuarios").select("usuario").eq("id", user_id).single().execute()
    return response.data["usuario"]