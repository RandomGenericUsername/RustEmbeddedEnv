
from dataclasses import dataclass, field
from typing import Union, List, Dict, Optional, Any, TypeVar, Callable
from constants import DIRECTORIES, MEMORY_UNITS, MEMORY_DIGITS_RANGE
import re

T = TypeVar('T')

def validate_list_elements(field: List[Any], element_type: T, field_name: str, custom_validator: Callable[[Any, str], None] = None, to_each: Optional[bool] = False):
    """
    Validates that the field is a list and that each element in the list is of the specified element type.
    Optionally applies a custom validation function to each element.

    :param field: The list to validate.
    :param element_type: The expected type of each element in the list.
    :param field_name: The name of the field (used for error messages).
    :param custom_validator: An optional callable that applies additional validation to each element.
    """
    if not isinstance(field, list):
        raise ValueError(f"Field {field_name} must be a list, got {type(field).__name__}")

    for item in field:
        if not isinstance(item, element_type):
            raise ValueError(f"Each item in field {field_name} must be of type {element_type.__name__}, got {type(item).__name__}")
        
        if custom_validator and to_each:
            custom_validator(item, field_name)

    if custom_validator:
        custom_validator(field, field_name)


def validate_non_empty(value: Any, field_name: str) -> None:
    # Check for None
    if value is None:
        raise ValueError(f"{field_name} key not set or is empty. Got: None")
    # Check for empty string or list directly
    if isinstance(value, (str, list)) and len(value) == 0:
        raise ValueError(f"{field_name} key not set or is empty. Got: {value}")

def validate_field_type(field: Any, field_type: Any, field_name: str) -> None:
      # Check if the field is of the expected base type (e.g., list, dict, custom class, etc.)
    if not isinstance(field, field_type):
        raise ValueError(f"Field {field_name} must be of type {field_type.__name__}, got {type(field).__name__}")


def validate_hexadecimal(value: str, field_name: str, digits_range: Optional[Dict[str, int]] = MEMORY_DIGITS_RANGE) -> None:
    # Use an f-string to insert the digits range variables into the regex pattern
    lower = digits_range.get("lower", 8)
    upper = digits_range.get("upper", 8)
    
    # Use an f-string to insert the digits range variables into the regex pattern
    if not re.match(rf'^0x[0-9A-Fa-f]{{{lower},{upper}}}$', value):
        raise ValueError(f"{field_name} must be a hexadecimal number with digits between {lower} and {upper}, got: {value}")



def validate_memory_size(value: str, field_name: str, memory_units : Optional[list[str]] = MEMORY_UNITS) -> None:

     # Build the regex pattern dynamically to include all units.
    # Note: The pattern checks for a numeric value followed by one of the units, case-insensitive.
    pattern = rf'^[0-9]*[02468](?:{"|".join(memory_units)})$'  # Matches an even number followed by a unit.
     # Validate the format is a number followed by a valid unit, case-insensitive.
    if not re.match(pattern, value, re.IGNORECASE):
        raise ValueError(f"{field_name} must be a string representing an even-numbered memory size followed by one of {', '.join(memory_units)} units, got: {value}")




def validate_memory_section(section: List[str], section_name: str) -> None:
    if len(section) != 2:
        raise ValueError(f"memory section: {section_name} must be exactly a list where the first element is the {section_name} origin and the second element is {section_name} length")
    validate_hexadecimal(section[0], f"{section_name}[0] (origin)")
    validate_memory_size(section[1], f"{section_name}[1] (length)")


@dataclass
class OpenOCDCfg:
    interface: str
    target: str
    def __post_init__(self):
        validate_non_empty(self.interface, "interface")
        validate_non_empty(self.target, "target")
        validate_field_type(self.interface, str, "interface")
        validate_field_type(self.target, str, "target")

@dataclass
class ExtraMemorySection:
    memory_type : str
    origin: str 
    length: str 

    def __post_init__(self):
        validate_non_empty(self.memory_type, "memory_type")
        validate_non_empty(self.origin, "origin")
        validate_non_empty(self.length, "length")
        validate_field_type(self.memory_type, str, "memory_type")
        validate_field_type(self.origin, str, "origin")
        validate_field_type(self.length, str, "length")
        validate_hexadecimal(self.origin, "origin")
        validate_memory_size(self.length, "length")

    def serialize(self) -> dict:
        return {"memory_type" : self.memory_type, "origin" : self.origin, "length" : self.length}


@dataclass
class MemoryConfig:
    flash: List[str] 
    ram: List[str]

    #optionals
    extra_sections: Optional[List[ExtraMemorySection]] = None

    def __post_init__(self):
        validate_non_empty(self.flash, "flash")
        validate_non_empty(self.ram, "ram")
        validate_list_elements(self.flash, str, "flash", validate_memory_section)
        validate_list_elements(self.ram, str, "ram", validate_memory_section)
        if self.extra_sections is not None:
            validate_list_elements(self.extra_sections, ExtraMemorySection, "extra_sections")

    def serialize(self) -> dict:
        return {"flash" : self.flash, "ram" : self.ram, "extra_sections" : [extra_section.serialize() for extra_section in self.extra_sections] if self.extra_sections is not None else None}

@dataclass
class CoreConfig:
    core: str
    arch: str
    memory: MemoryConfig
    openocd_cfg: OpenOCDCfg

    ###
    debug_configuration: Optional[str] = None

    def __post_init__(self)-> None:
        validate_non_empty(self.core, "core")
        validate_non_empty(self.arch, "arch")
        validate_non_empty(self.memory, "memory")
        validate_non_empty(self.openocd_cfg, "openocd_cfg")
        validate_field_type(self.core, str, "core")
        validate_field_type(self.arch, str, "arch")
        validate_field_type(self.memory, MemoryConfig, "memory")
        validate_field_type(self.openocd_cfg, OpenOCDCfg, "openocd_cfg")
        if self.debug_configuration:
            validate_non_empty(self.debug_configuration, "debug_configuration")
            validate_field_type(self.debug_configuration, str, "debug_configuration")


    def serialize(self) -> dict:
        return {"core" : self.core, "arch" : self.arch, "memory" : self.memory.serialize(), "debug_configuration" : self.debug_configuration }


@dataclass
class ProjectConfig:
    mcu_family: str
    config: List[CoreConfig]
    # Optionals
    directories: Optional[List[str]] = None 
    arch: Optional[str] = None
    debug_configuration: Optional[str] = None


    def __post_init__(self)-> None:
        validate_non_empty(self.mcu_family, "mcu_family")
        validate_non_empty(self.config, "config")
        validate_field_type(self.mcu_family, str, "mcu_family")
        validate_list_elements(self.config, CoreConfig, "config")
        if self.directories:
            validate_non_empty(self.directories, "directories")
            validate_list_elements(self.directories, str, "directories")
        if self.arch:
            validate_non_empty(self.arch, "arch")
            validate_field_type(self.arch, str, "arch")
        if self.debug_configuration:
            validate_non_empty(self.debug_configuration, "debug_configuration")
            validate_field_type(self.debug_configuration, str, "debug_configuration")

    def serialize(self) -> dict:
        return {"mcu_family": self.mcu_family, "config" : [c.serialize() for c in self.config], "directories" : self.directories, "arch" : self.arch, "debug_configuration" : self.debug_configuration}

    @property
    def get(self) -> dict:
        return self.serialize()
