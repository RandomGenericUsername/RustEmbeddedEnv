#!/usr/bin/python3

from typing import List, Tuple
import sys
import os
import json

from project_creator import project_creator 
from project_types import ProjectConfig, MemoryConfig

# Update the system path to include the parent directory of the current script
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

def load_config_from_json(file_path: str) -> ProjectConfig:

    # Check if the file exists
    if not os.path.isfile(file_path):
        print(f"Error: The specified file '{file_path}' does not exist.")
        sys.exit(1)

    try:
        with open(file_path, "r") as f:
            config_data = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: The file '{file_path}' is not a valid JSON file.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: Unable to load the configuration file '{file_path}': {e}")
        sys.exit(1)


    data = config_data["memory"]
    memory_config = MemoryConfig(
        flash_origin=data["flash_origin"],
        flash_end=data["flash_end"],
        ram_origin=data["ram_origin"],
        ram_end=data["ram_end"],
    )
    return ProjectConfig(
        mcu_family=config_data["mcu_family"],
        cores=config_data["cores"],
        arch=config_data["arch"],
        memory=memory_config,
    )

def parse_arguments(args: List[str]) -> Tuple[str, ProjectConfig]:
    if len(args) != 2:
        print("Usage: ./create_project.py project_name config.json")
        sys.exit(1)
    project_name = args[0]
    config_file_path = args[1]
    project_config = load_config_from_json(config_file_path)
    return project_name, project_config


if __name__ == "__main__":
    project_name, config = parse_arguments(sys.argv[1:])
    if not config.validate():
        print("Error: Invalid project configuration.")
        sys.exit(1)
    project_creator(project_name, config)