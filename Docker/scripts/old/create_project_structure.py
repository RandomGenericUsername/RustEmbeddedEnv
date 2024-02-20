import subprocess
import os


def create_project_directories(path: str, directories: list[str]) -> None:
    # Loop through the list of directories and create each one
    for directory in directories:
        # Construct the path for each directory
        dir_path = os.path.join(path, directory)
        # Make the directory, including intermediate directories as needed
        os.makedirs(dir_path, exist_ok=True)
        print(f"Directory: {directory} created successfully at path: {path}.")

def generate_rust_project(path: str, project_name: str):
    try:
        # Construct the command as a list of its parts
        command = [
            "cargo", "generate",
            "--git", "https://github.com/rust-embedded/cortex-m-quickstart",
            "--name", project_name,
            "--destination", path
        ]

        # Execute the command
        result = subprocess.run(command, check=True, capture_output=True, text=True)

        # Check if the command was successful
        if result.returncode == 0:
            print(f"Project {project_name} generated successfully at path {path}.")
            print(result.stdout)  # Print the stdout of the command
        else:
            print("Error in generating project:")
            print(result.stderr)  # Print the stderr of the command

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while trying to generate the project: {e}")