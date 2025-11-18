import shutil
from pathlib import Path

# db and storage resources handling
async def make_folder(local_storage_path: str):
    Path(local_storage_path).mkdir(parents=True, exist_ok=True)
    print(f"Directory '{local_storage_path}' created successfully.")

async def remove_folder(local_storage_path: str):
    directory_to_remove = Path(local_storage_path)
    if Path(local_storage_path).is_dir():
        try:
            shutil.rmtree(directory_to_remove)
            print(f"Directory '{directory_to_remove}' and its contents removed successfully.")
        except OSError as e:
            print(f"Error: {e.strerror} - Could not remove directory '{directory_to_remove}'.")
    else:
        print(f"Directory '{directory_to_remove}' does not exist.")

### Others ###
def parse_boolean(value):
    if value is None:
        return False
    return value.lower() in ('true', '1', 'yes', 'on')
