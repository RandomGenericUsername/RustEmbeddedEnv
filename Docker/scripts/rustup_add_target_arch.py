import subprocess

def rustup_add_target_arch(arch: str) -> None:
    command = ["rustup", "target", "add", arch]
    try:
        # Run the command and wait for it to complete
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"Command executed successfully: {result.stdout}")
    except subprocess.CalledProcessError as e:
        # Handle errors in the subprocess
        print(f"An error occurred: {e.stderr}")
