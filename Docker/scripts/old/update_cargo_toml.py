import os
import re


def update_cargo_toml(path: str, file_name: str, arch: str, mcu_family: str, debugger_option: str):
    file_path = os.path.join(path, file_name)
    if not os.path.isfile(file_path):
        print(f"The file does not exist: {file_path}")
        return
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    new_lines = []
    build_section_found = False
    arch_already_exists = False
    correct_arch_set = False

    # Regex to match the architecture line precisely, with optional leading whitespace
    arch_regex = re.compile(r'^\s*#\s*target\s*=\s*"' + re.escape(arch) + r'"\s*(#.*)?$')
    target_line_format = f'target = "{arch}" # {mcu_family}\n'

    for line in lines:
        # Uncomment the specified debugger option
        if 'runner =' in line and debugger_option in line and line.strip().startswith('#'):
            line = line.lstrip('#').lstrip()

        # Process [build] section for the architecture
        if '[build]' in line:
            build_section_found = True
        elif build_section_found:
            if arch_regex.match(line):
                # Uncomment the existing architecture line if it matches
                line = f"target = \"{arch}\" # {mcu_family}\n"
                correct_arch_set = True
                arch_already_exists = True
            elif 'target =' in line and not correct_arch_set:
                # Comment out any other architecture
                line = f"# {line}" if not line.strip().startswith('#') else line
            elif line.strip().startswith('[') and not correct_arch_set:
                # If exiting the build section without setting the correct architecture, add it
                if not arch_already_exists:
                    new_lines.append(target_line_format)
                    correct_arch_set = True
                build_section_found = False
        
        new_lines.append(line)

    if build_section_found and not correct_arch_set and not arch_already_exists:
        # If the file ends without another section starting after [build] and arch not set, add it
        new_lines.append(target_line_format)

    with open(file_path, 'w') as file:
        file.writelines(new_lines)
    print(f"Configuration updated in {file_path}.")
