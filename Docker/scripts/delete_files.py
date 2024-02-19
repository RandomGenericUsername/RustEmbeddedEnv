import os
import shutil

def delete_files_and_directories(path: str, names_to_delete: list):
    # Change to the specified directory
    original_path = os.getcwd()  # Remember the original path to restore later
    try:
        os.chdir(path)
        print(f"Changed directory to {path}")

        # Iterate through each name in the list
        for name in names_to_delete:
            if os.path.exists(name):
                # Check if it's a file or directory and delete accordingly
                if os.path.isfile(name):
                    os.remove(name)
                    print(f"Deleted file: {name}")
                elif os.path.isdir(name):
                    shutil.rmtree(name)
                    print(f"Deleted directory: {name}")
            else:
                print(f"{name} does not exist in {path}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Restore the original working directory
        os.chdir(original_path)
        print(f"Restored directory to {original_path}")
