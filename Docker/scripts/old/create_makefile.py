import os

def create_file(path: str, file_name: str):

    file_path = os.path.join(path, file_name)
    # Check if the file already exists
    if not os.path.exists(file_path):
        # Extract the directory path
        dir_path = os.path.dirname(file_path)
        
        # If the directory path is not empty and does not exist, create it
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"Directory {dir_path} created.")
        
        # Create the file
        with open(file_path, 'w') as file:
            pass  # Just create the file, don't write anything
        print(f"File {file_path} created.")
    else:
        print(f"File {file_path} already exists.")


def create_makefile(path: str, name: str, rules):
    # Construct the full path for the Makefile
    makefile_path = os.path.join(path, name)
    
    with open(makefile_path, 'w') as makefile:
        for rule, details in rules.items():
            # Write rule name and potentially dependencies
            if isinstance(details, dict) and 'dependencies' in details:
                makefile.write(f"{rule}: {' '.join(details['dependencies'])}\n")
            else:
                makefile.write(f"{rule}:\n")
            
            # Determine the command(s) to write
            commands = details.get('command') if isinstance(details, dict) else details
            if isinstance(commands, str):
                commands = [commands]  # Wrap single command in a list for consistency
            
            # Write each command on a new line, properly indented
            for command in commands:
                makefile.write(f"\t{command}\n")
            makefile.write("\n")  # Add a newline for spacing between rules
    
    print(f"Makefile created at {makefile_path}")

## Example usage
#core_path = '/path/to/directory'
#rules = {
#    'all': {
#        'dependencies': ['clean', 'build'],
#        'command': ['echo "Cleaning..."', 'echo "Building all targets"']
#    },
#    "build": ["echo 'Building target'", "cargo build"],
#    'clean': ['echo "Cleaning up"', 'cargo clean']
#}
#create_makefile(core_path, 'Makefile', rules)


def append_rules_to_makefile(path: str, name: str, new_rules):
    # Construct the full path for the Makefile
    makefile_path = os.path.join(path, name)
    
    # Read the existing Makefile content
    if os.path.isfile(makefile_path):
        with open(makefile_path, 'r') as file:
            existing_content = file.read()
    else:
        print(f"The file does not exist: {makefile_path}")
        return
    
    # Check if the rule already exists to avoid duplication
    existing_rules = set(line.split(':')[0].strip() for line in existing_content.splitlines() if ':' in line)

    # Append new rules to the Makefile
    with open(makefile_path, 'a') as makefile:
        for rule, details in new_rules.items():
            if rule not in existing_rules:
                # Write rule name and potentially dependencies
                if isinstance(details, dict) and 'dependencies' in details:
                    makefile.write(f"\n{rule}: {' '.join(details['dependencies'])}\n")
                else:
                    makefile.write(f"\n{rule}:\n")
                
                # Determine the command(s) to write
                commands = details.get('command') if isinstance(details, dict) else details
                if isinstance(commands, str):
                    commands = [commands]  # Wrap single command in a list for consistency
                
                # Write each command on a new line, properly indented
                for command in commands:
                    makefile.write(f"\t{command}\n")
            else:
                print(f"Rule '{rule}' already exists in the Makefile and was not added.")
    
    print(f"New rules appended to {makefile_path}")

## Example usage
#core_path = '/path/to/directory'
#name = 'Makefile'
#new_rules = {
#    'test': {
#        'dependencies': ['clean'],
#        'command': 'echo "Running tests"'
#    },
#    "deploy": "echo 'Deploying application'"
#}
#append_rules_to_makefile(core_path, name, new_rules)

def sanitize_rule_name(core):
    """
    Sanitizes the core name to be used as a Makefile rule name.
    
    Args:
    - core (str): The core name, which may contain hyphens, underscores, or colons.
    
    Returns:
    - str: A sanitized version of the core name suitable for a Makefile rule.
    """
    # Replace colons with underscores to avoid syntax issues in Makefiles
    sanitized_name = core.replace(':', '_')
    
    # Further sanitization can be added here if needed

    return sanitized_name

## Example usage
#cores = ['cortex-m7', 'cortex_m7', 'cortex:m7']
#for core in cores:
#    rule_name = sanitize_rule_name(core)
#    print(f"Original: {core}, Makefile rule name: {rule_name}")


def prepend_variables_to_makefile(path: str, file_name: str, variables):
    makefile_path = os.path.join(path, file_name)
    # Read the existing Makefile content
    if os.path.isfile(makefile_path):
        with open(makefile_path, 'r') as file:
            existing_content = file.read()
    else:
        print(f"The file does not exist: {makefile_path}")
        return
    
    # Prepare the new content to be added
    new_content = ""
    for var_name, details in variables.items():
        if isinstance(details, dict):
            # Extract value and optional operator
            value = details.get("value", "")
            operator = details.get("operator", ":=")  # Default operator
        else:
            # If details is directly the value, use the default operator
            value = details
            operator = ":="
        
        # Append the variable declaration to the new content
        new_content += f"{var_name} {operator} {value}\n"
    
    # Prepend the new content to the existing content
    updated_content = new_content + "\n" + existing_content
    
    # Write the updated content back to the Makefile
    with open(makefile_path, 'w') as file:
        file.write(updated_content)
    
    print(f"Variables added to {makefile_path}")

## Example usage
#makefile_path = 'path/to/Makefile'
#variables = {
#    "SUBDIR": {"value": "Core/m4 Core/m7", "operator": ":="},
#    "ANOTHER_VAR": "Some Value"
#}
#prepend_variables_to_makefile(makefile_path, variables)
