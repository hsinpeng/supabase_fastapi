from supabase import create_client

if __name__ == "__main__":
    url = ""
    key = ""
    
    supabase = create_client(url, key)
    data = supabase.table("users").select("*").execute()
    print(data)