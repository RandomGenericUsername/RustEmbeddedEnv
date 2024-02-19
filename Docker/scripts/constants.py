DIRECTORIES = ["Common", "Drivers", "Utils"]
DIRECTORIES_TO_DELETE_FROM_TEMPLATE = ["examples"]
MEMORY_UNITS = ["K"]
MEMORY_DIGITS_RANGE = {"lower" : 6, "upper" : 8}
LINES_TO_DELETE_FROM_MEMORY_X_FILE = [
    "/* These values correspond to the LM3S6965, one of the few devices QEMU can emulate */"
]



### Default debug configuration
#debugger_option = "<option>"  
# Options: "arm-none-eabi-gdb"
# Options: "gdb-multiarch"
# Options: "gdb"
DEFAULT_DEBUGGER_CONFIGURATION = 'gdb-multiarch'


