import os

def update_openocd_cfg(path: str, header: str, interface_cfg: str, target_cfg: str):
    # Check if the file exists
    file_path = os.path.join(path, 'openocd.cfg')
    if not os.path.isfile(file_path):
        print(f"The file does not exist at the specified path: {file_path}")
        return
    
    # Read the file contents
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Update the file contents
    new_lines = []
    for line in lines:
        if line.startswith("# Sample OpenOCD configuration"):
            new_lines.append(f"# {header}\n")
        elif "interface/" in line:
            new_lines.append(line.replace("stlink.cfg", interface_cfg))
        elif "target/" in line:
            new_lines.append(line.replace("stm32f3x.cfg", target_cfg))
        else:
            new_lines.append(line)
    
    # Write the modified contents back to the file
    with open(file_path, 'w') as file:
        file.writelines(new_lines)
    print(f"OpenOCD configuration file updated successfully at {file_path}")


