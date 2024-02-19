import os
from utils import normalize_string


from constants import (
    DIRECTORIES,
    DEFAULT_DEBUGGER_CONFIGURATION,
    DIRECTORIES_TO_DELETE_FROM_TEMPLATE,
)
from project_types import ProjectConfig, CoreConfig
from update_memory import modify_memory_x
from update_openocd_cfg import update_openocd_cfg
from rustup_add_target_arch import rustup_add_target_arch
from delete_files import delete_files_and_directories
from update_cargo_toml import update_cargo_toml
from create_makefile import (
    create_makefile,
    append_rules_to_makefile,
    create_file,
    sanitize_rule_name,
    prepend_variables_to_makefile,
)
from create_project_structure import generate_rust_project, create_project_directories


def project_creator(project_name: str, project_config: ProjectConfig) -> None:

    # Raw variables
    mcu_family = project_config.mcu_family
    configs = project_config.config
    user_defined_directories = project_config.directories

    ###
    project_dirs = DIRECTORIES + (user_defined_directories or [])
    # Normalize the project name
    normalized_project_name = normalize_string(
        input_str=project_name, chars_to_normalize=[":"], normalizer="_"
    )
    # This variable will load the directories that will be created within the root of the project
    project_path = os.path.join(os.getcwd(), normalized_project_name)
    include_makefile_var = ""

    # Create a directory named as 'normalized_project_name' in the current location, containing in the root the directories' names passed on respective argument
    create_project_directories(path=project_path, directories=project_dirs)
    # Create global makefile
    create_file(path=project_path, file_name="Makefile")
    # Navigate to the created directory
    # os.chdir(project_path)
    cores_rules = []

    for config in configs:
        # Creates the main project files for each core
        normalized_core_name = normalize_string(
            input_str=config.core, chars_to_normalize=[":", "_"], normalizer="-"
        )
        core_path = os.path.join(project_path, normalized_core_name)
        generate_rust_project(path=project_path, project_name=normalized_core_name)
        # os.chdir(core_path)
        modify_memory_x(
            path=core_path, mcu_family=mcu_family, config=config, file_name="memory.x"
        )
        update_openocd_cfg(
            path=core_path,
            header=f"Configuration for {mcu_family}",
            interface_cfg="stlink.cfg",
            target_cfg="stm32h7x_dual_bank.cfg",
        )
        rustup_add_target_arch(arch=config.arch)
        delete_files_and_directories(
            path=core_path, names_to_delete=DIRECTORIES_TO_DELETE_FROM_TEMPLATE
        )

        core_debugger_option = (
            DEFAULT_DEBUGGER_CONFIGURATION
            if (dbg := config.debug_configuration is None)
            else dbg
        )
        core_arch = (
            project_config.arch if project_config.arch is not None else config.arch
        )
        debugger_option = (
            core_debugger_option
            if project_config.debug_configuration is None
            else project_config.debug_configuration
        )
        update_cargo_toml(
            path=os.path.join(core_path, ".cargo"),
            file_name="config.toml",
            arch=core_arch,
            mcu_family=mcu_family,
            debugger_option=debugger_option,
        )
        rules = {
            "all": {
                "dependencies": ["clean", "build"],
                "command": ['echo "Cleaning..."', 'echo "Building all targets"'],
            },
            "build": ["echo 'Building target'", "cargo build"],
            "clean": ['echo "Cleaning up"', "cargo clean"],
        }
        create_makefile(path=core_path, name="Makefile", rules=rules)

        build_core_rule = f"build-{normalized_core_name}"
        clean_core_rule = f"clean-{normalized_core_name}"
        all_core_rule = f"all-{normalized_core_name}"

        global_rules = {
            build_core_rule : f"$(MAKE) -C {normalized_core_name} build",
            clean_core_rule : f"$(MAKE) -C {normalized_core_name} clean",
            all_core_rule : f"$(MAKE) -C {normalized_core_name} all",
        }
        include_makefile_var = include_makefile_var + f"{normalized_core_name} "
        append_rules_to_makefile(
            path=project_path, name="Makefile", new_rules=global_rules
        )
        cores_rules.append((build_core_rule, clean_core_rule, all_core_rule))

        # Leave directory
        os.chdir(project_path)

    # Add subdirs to global makefile
    prepend_variables_to_makefile(path=project_path, file_name= 'Makefile', variables={"SUBDIRS" : include_makefile_var})

    build_rule_dependencies = [core_rule[0] for core_rule in cores_rules]  # Extract build_core_rule for each core
    clean_rule_dependencies = [core_rule[1] for core_rule in cores_rules]  # Extract build_core_rule for each core
    all_rule_dependencies = [core_rule[2] for core_rule in cores_rules]  # Extract build_core_rule for each core

    rules = {
        "build" : { "dependencies" : build_rule_dependencies, "command" : "echo 'building for both cores'"},
        "clean" : { "dependencies" : clean_rule_dependencies, "command" : "echo 'cleaning for both cores'"},
        "all"   : { "dependencies" : all_rule_dependencies,   "command" : "echo 'building and cleaning for both cores'"},
    }
    append_rules_to_makefile(path=project_path, name='Makefile', new_rules=rules)

