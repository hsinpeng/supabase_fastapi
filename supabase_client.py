import os
from dotenv import load_dotenv
from supabase import create_client

if __name__ == "__main__":
    load_dotenv("setting/.env.dev")
    supabase_url:str = os.getenv("SUPABASE_URL")
    supabase_key:str = os.getenv("SUPABASE_KEY")
    
    supabase = create_client(supabase_url, supabase_key)
    data = supabase.table("users").select("*").execute()
    print(data)