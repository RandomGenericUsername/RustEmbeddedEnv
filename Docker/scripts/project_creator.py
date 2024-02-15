import os
import json
from typing import List

from constants import DIRECTORIES
from project_types import ProjectConfig


def project_creator(project_name: str, project_config: ProjectConfig) -> None:
    # You can add your project creation logic here
    mcu_family = project_config.mcu_family
    print(f"Creating project '{project_name}' for MCU family '{mcu_family}'.")

    directories = DIRECTORIES

    # Loop through the list of directories and create each one
    for directory in directories:
        # Construct the path for each directory
        dir_path = os.path.join(project_name, directory)

        # Make the directory, including intermediate directories as needed
        os.makedirs(dir_path, exist_ok=True)
    print(f"Basic project structure for '{project_name}' created successfully.")

