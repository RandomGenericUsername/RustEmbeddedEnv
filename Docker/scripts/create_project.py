#!/usr/bin/python3

from typing import List, Dict, Optional, Tuple, Union
import sys
import os
import json
from project_creator import project_creator
from project_types import ProjectConfig, MemoryConfig, ExtraMemorySection, CoreConfig

def add_to_sys_path():
    current_dir = os.path.dirname(__file__)
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(parent_dir)

def validate_file_exists(file_path: str):
    if not os.path.isfile(file_path):
        print(f"Error: The specified file '{file_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

def load_json_data(file_path: str) -> Dict:
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Error: The file '{file_path}' is not a valid JSON file.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: Unable to load the configuration file '{file_path}': {e}", file=sys.stderr)
        sys.exit(1)

def create_extra_memory_sections(extra_sections: Union[Dict, List[Dict]]) -> List[ExtraMemorySection]:
    if extra_sections is None:
        return None

    if isinstance(extra_sections, dict):
        extra_sections = [extra_sections] 

    return [
        ExtraMemorySection(
            memory_type=section.get("memory_type", None),
            origin=section.get("origin", None),
            length=section.get("length", None)
        ) for section in extra_sections 
    ]

def create_memory_config(memory_config: Dict) -> MemoryConfig:
    if memory_config is None:
        return None
    return MemoryConfig(
        flash=memory_config.get("flash", None),
        ram=memory_config.get("ram", None),
        extra_sections=create_extra_memory_sections(memory_config.get('extra_sections', None))
    )


def create_core_configs(configs: Dict) -> List[CoreConfig]:
    if configs is None:
        return None

    # Check if the config_section is a dictionary (single core), and if so, wrap it in a list.
    if isinstance(configs, dict):
        configs = [configs]  # Make it a list of one dictionary.
    # Proceed with creating CoreConfig objects.
    return [
        CoreConfig(
            core=config.get("core", None),
            arch=config.get("arch", None),
            memory=create_memory_config(config.get("memory", None)),
            debug_configuration=config.get('debug_configuration', None)
        ) for config in configs  # This now works for both single and multiple configs.
    ]


def load_config_from_json(file_path: str) -> ProjectConfig:
    validate_file_exists(file_path)
    config_data = load_json_data(file_path)

    return ProjectConfig(
        mcu_family=config_data.get("mcu_family", None),
        config=create_core_configs(config_data.get('config', None)),
        directories=config_data.get("directories", None),
        arch=config_data.get("arch", None),
        debug_configuration=config_data.get("debug_configuration", None)
    )

def parse_arguments(args: List[str]) -> Tuple[str, ProjectConfig]:
    if len(args) != 2:
        print("Usage: ./create_project.py project_name config.json", file=sys.stderr)
        sys.exit(1)
    project_name, config_file_path = args
    project_config = load_config_from_json(config_file_path)
    return project_name, project_config

if __name__ == "__main__":
    add_to_sys_path()
    project_name, config = parse_arguments(sys.argv[1:])
    project_creator(project_name, config)
