import os
from dotenv import load_dotenv
from supabase import create_client, Client

def sign_up_user(supabase:Client, email:str, password:str):
    try:
        response = supabase.auth.sign_up({"email": email, "password": password})
        if response.user:
            print(f"User {response.user.email} signed up successfully!")
            #print(response)
            return response.user
        else:
            print(f"Sign up error: {response.session}") # Check response.session for error details
            return None
    except Exception as e:
        print(f"An error occurred during sign up: {e}")
        return None


def sign_in_user(supabase:Client, email:str, password:str):
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if response.user:
            print(f"User {response.user.email} signed in successfully!")
            print(response)
            return response.user
        else:
            print(f"Sign in error: {response.session}") # Check response.session for error details
            return None
    except Exception as e:
        print(f"An error occurred during sign in: {e}")
        return None


def sign_out_user(supabase:Client)->bool:
    try:
        response = supabase.auth.sign_out()
        if response is None:
            print("User signed out successfully!")
            return True
        else:
            print(f"Sign out error: {response}")
            return False
    except Exception as e:
        print(f"An error occurred during sign out: {e}")
        return False

def display_session(supabase:Client)->bool:
    # Retrieve the session data
    response = supabase.auth.get_session()
    if response:
        print("User is signed in.")
        print("Token Type:", response.token_type)
        print("Access Token:", response.access_token)
        print("Refresh Token:", response.refresh_token)
        print("User ID:", response.user.id)
        print("User Email:", response.user.email)
        print("User Aud:", response.user.aud)
        return True
    else:
        print("No active session found.")
        return False
    

def db_crud_with_user_id(supabase:Client, user_id:str):
    # Insert a task
    new_task = {"title": "Learning", "description": "Learn Self-hosted Supabase with Python", "user_id": user_id}
    response = supabase.table("tasks").insert(new_task).execute()
    print("Created:", response.data)
    print("-------------------------------")

    # Read all tasks
    all_tasks = supabase.table("tasks").select("*").execute()
    print("All Tasks:", all_tasks.data)
    print("-------------------------------")

    # Read a specific task by ID
    specific_task_id = all_tasks.data[0]['id'] if all_tasks.data else None # Assuming at least one todo exists
    if specific_task_id:
        single_task = supabase.table("tasks").select("*").eq("id", specific_task_id).execute()
        print(f"Specific Task ({specific_task_id}):", single_task.data)
    print("-------------------------------")

    # Update a task
    if specific_task_id:
        updated_task = {"description": "Master Supabase with Python!"}
        response = supabase.table("tasks").update(updated_task).eq("id", specific_task_id).execute()
        print("Updated:", response.data)
    print("-------------------------------")

    # Delete a task
    if specific_task_id:
        response = supabase.table("tasks").delete().eq("id", specific_task_id).execute()
        print("Deleted:", response.data)
    print("-------------------------------")


def main():
    # Initialization
    load_dotenv("setting/.env.dev")
    supabase_url:str = os.getenv("SUPABASE_URL")
    supabase_key:str = os.getenv("SUPABASE_KEY")
    supabase_client:Client = create_client(supabase_url, supabase_key)

    # Authentication Settings
    username:str = "wenli07@yahoo.com.tw"
    password:str = "password123"
    
    # Testing
    run_opt:int = 2
    match run_opt:
        case 1:
            print(f"run_opt={run_opt}: Authentication(sign up)")
            user = sign_up_user(supabase_client, username, password)
            if user:
                print(f"Sing up OK! Current user ID: {user.id}")
            else:
                print(f"Error: Sing up failure!")
            print("-------------------------------")

        case 2:
            print(f"run_opt={run_opt}: Authentication(sign in/out)")
            # Sign in a user
            user = sign_in_user(supabase_client, username, password)
            if user:
                print(f"Sing in OK! Current user ID: {user.id}")
            else:
                print(f"Error: Sing in failure!")
            print("-------------------------------")

            display_session(supabase_client)
            print("-------------------------------")

            db_crud_with_user_id(supabase_client, user.id)
            print("-------------------------------")

            # Sign out the user
            result:bool = sign_out_user(supabase_client)
            if result:
                print(f"Sing out OK! user ID: {user.id}")
            else:
                print(f"Error: Sing out failure!")
            print("-------------------------------")

            display_session(supabase_client)
            print("-------------------------------")

        case 3:
            print(f"run_opt={run_opt}: DB CRUD")
            display_session(supabase_client)
            print("-------------------------------")

            data = supabase_client.table("tasks").select("*").execute()
            print(data)
            print("-------------------------------") 
            
        case _:
            print(f"Error: no run_opt={run_opt}")

if __name__ == "__main__":
    main()
