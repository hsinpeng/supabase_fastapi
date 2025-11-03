#from contextlib import asynccontextmanager
import shutil
from pathlib import Path
from utilities.config import get_settings

settings = get_settings()

# db and storage resources handling
async def init_db_storage():
    Path(settings.local_storage_path).mkdir(parents=True, exist_ok=True)
    print(f"Directory '{settings.local_storage_path}' created successfully.")

async def close_db_storage():
    directory_to_remove = Path(settings.local_storage_path)
    if Path(settings.local_storage_path).is_dir():
        try:
            shutil.rmtree(directory_to_remove)
            print(f"Directory '{directory_to_remove}' and its contents removed successfully.")
        except OSError as e:
            print(f"Error: {e.strerror} - Could not remove directory '{directory_to_remove}'.")
    else:
        print(f"Directory '{directory_to_remove}' does not exist.")

# database

