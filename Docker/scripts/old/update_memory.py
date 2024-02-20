import re
import os
from typing import List, Optional
from project_types import CoreConfig
from constants import LINES_TO_DELETE_FROM_MEMORY_X_FILE


def modify_memory_x(path: str, mcu_family: str, config: CoreConfig, lines_to_delete: Optional[list] = LINES_TO_DELETE_FROM_MEMORY_X_FILE, file_name : Optional[str] = 'memory.x'):
    memory_x_path = os.path.join(path, file_name)
    replaces = [(
        "  /* TODO Adjust these memory regions to match your device memory layout */ ",
        f"/* Values adjusted for {mcu_family} */"
    )]
    # Check if the file exists
    if os.path.isfile(memory_x_path):
        lines = read_file_contents(memory_x_path)
        lines = delete_lines(lines, lines_to_delete)
        lines = update_flash_and_ram(lines, config)
        lines = add_extra_memory_sections(lines, config)
        lines = replace_lines(lines, replaces)
        write_file_contents(memory_x_path, lines)
    else:
        print(f"The file {file_name} does not exist at the specified path: {path}.")


def read_file_contents(file_path: str):
    with open(file_path, 'r') as file:
        return file.readlines()

def write_file_contents(file_path: str, lines):
    with open(file_path, 'w') as file:
        file.writelines(lines)

def delete_lines(lines, lines_to_delete):
    return [line for line in lines if line.strip() not in lines_to_delete]

def update_flash_and_ram(lines, config):
    new_lines = []
    for line in lines:
        if "FLASH :" in line:
            line = f"  FLASH : ORIGIN = {config.memory.flash[0]}, LENGTH = {config.memory.flash[1]}\n"
        elif "RAM :" in line:
            line = f"  RAM : ORIGIN = {config.memory.ram[0]}, LENGTH = {config.memory.ram[1]}\n"
        new_lines.append(line)
    return new_lines

def add_extra_memory_sections(lines, config):
    if hasattr(config.memory, 'extra_sections') and config.memory.extra_sections:
        extra_section_lines = [
            f"  {section.memory_type.upper()} : ORIGIN = {section.origin}, LENGTH = {section.length}\n"
            for section in config.memory.extra_sections
        ]
        
        memory_block_start_found = False
        memory_block_end_index = None
        for i, line in enumerate(lines):
            if 'MEMORY' in line:
                memory_block_start_found = True
            elif memory_block_start_found and '{' in line:
                # Adjust to handle MEMORY block start correctly when '{' is on a separate line
                memory_block_start_index = i
            elif memory_block_start_found and '}' in line:
                memory_block_end_index = i
                break  # Stop after finding the end of the MEMORY block
        
        if memory_block_end_index is not None:
            # Insert the extra sections before the MEMORY block's closing brace
            lines = lines[:memory_block_end_index] + extra_section_lines + lines[memory_block_end_index:]
        else:
            print("Failed to identify MEMORY block accurately. Extra sections not added.")
    return lines

def replace_lines(lines, replacement_tuples):
    """Replaces specified lines using regular expressions for flexible matching."""
    new_lines = []
    for line in lines:
        for original, replacement in replacement_tuples:
            # Create a regex pattern that matches the original string, ignoring extra whitespace
            pattern = re.compile(re.escape(original.strip()), re.IGNORECASE)
            if pattern.search(line.strip()):
                # Replace the matched part of the line with the replacement, maintaining the rest of the line unchanged
                line = pattern.sub(replacement, line)
                break
        new_lines.append(line)
    return new_lines
