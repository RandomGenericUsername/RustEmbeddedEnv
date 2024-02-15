from dataclasses import dataclass
from typing import Union, List, Dict

@dataclass
class MemoryConfig:
    flash_origin: Union[str, Dict[str, str]]
    flash_end: Union[str, Dict[str, str]]
    ram_origin: Union[str, Dict[str, str]]
    ram_end: Union[str, Dict[str, str]]


@dataclass
class ProjectConfig:
    mcu_family: str
    cores: Union[str, List[str]]
    arch: Union[str, List[str]]
    memory: MemoryConfig
    
    def validate(self) -> bool:
        valid = True  # Keep track of the overall validation status

        # Determine if we are working with a single core or multiple cores
        single_core = isinstance(self.cores, str) or (isinstance(self.cores, list) and len(self.cores) == 1)
        core_names = [self.cores] if isinstance(self.cores, str) else self.cores
        
        # Validate memory configurations based on single_core or multiple_cores
        memory_attributes = ['flash_origin', 'flash_end', 'ram_origin', 'ram_end']
        for attr in memory_attributes:
            value = getattr(self.memory, attr)
            
            if single_core:
                if not isinstance(value, str):
                    print(f"Validation Error: For a single core, '{attr}' must be a string, got {type(value).__name__} instead.")
                    valid = False
            else:
                if not isinstance(value, Dict):
                    print(f"Validation Error: For multiple cores, '{attr}' must be a dictionary, got {type(value).__name__} instead.")
                    valid = False
                elif len(value) != len(core_names):
                    print(f"Validation Error: '{attr}' must contain exactly {len(core_names)} keys for multiple cores, found {len(value)} keys.")
                    valid = False
                elif sorted(value.keys()) != sorted(core_names):
                    print(f"Validation Error: The keys in '{attr}' ({', '.join(sorted(value.keys()))}) do not match the specified core names ({', '.join(sorted(core_names))}).")
                    valid = False
        
        # Validate arch based on single_core or multiple_cores
        if single_core:
            if not isinstance(self.arch, str):
                print(f"Validation Error: For a single core, 'arch' must be a string, got {type(self.arch).__name__} instead.")
                valid = False
        else:
            if not isinstance(self.arch, List):
                print(f"Validation Error: For multiple cores, 'arch' must be a list of strings, got {type(self.arch).__name__} instead.")
                valid = False
            elif not all(isinstance(item, str) for item in self.arch):
                print("Validation Error: All items in 'arch' must be strings.")
                valid = False

        if not valid:
            print("ProjectConfig validation failed.")
            return False

        print("ProjectConfig validation passed.")
        return True
