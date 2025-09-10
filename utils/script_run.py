#.................................................
#   SCRIPT_RUN.PY, v2.0.0, December 2024, Domenico Lanza.
#.................................................
#   This module is used to detect if a scripted run 
#   must be executed.
#.................................................
from utils.classes import ProgramConstants

def script_file_detected():
    """This function checks if a script.pfs file is present 
    in the current directory.

    Returns:
        bool: True if the file is present, False otherwise
    """
    # Constants:
    program_constants = ProgramConstants()
    FILENAME = program_constants.ScriptRun.SCRIPT_FILENAME  # Default filename for the script file
    # Check if the file exists
    try:
        file = open(FILENAME, "r")
        file.close()
        return True
    except:
        return False

def retrieve_program_mode():
    """This function retrieve the program mode
    from the script.pfs file.

    Raises:
        ValueError: If the program mode is invalid
        FileError: If the script.pfs cannot be read

    Returns:
        program_mode (int): the program mode
    """
    # Constants:
    program_constants = ProgramConstants()
    FILENAME = program_constants.ScriptRun.SCRIPT_FILENAME  # Default filename for the script file
    # Try to open the file
    try:
        file = open(FILENAME, "r")
    except:
        raise Exception("FileError: The script.pfs file cannot be read.")
    line = file.readline()
    program_mode = line.split(":")[1].strip().lower()  # Take the part of the string after the ":", strip it and convert it to lowercase
    file.close() 
    match program_mode:  # Check if the program mode is valid, and return the corresponding integer
        case "srun":
            return 1
        case "xlsx":
            return 2
        case "in":
            return 3
        case _:
            raise ValueError("Invalid program mode.")

def retrieve_filename():
    """This function retrieves the input 
    filename from the script.pfs file.

    Returns:
        filename (string): the input filename
    """
    # Constants:
    program_constants = ProgramConstants()
    SCRIPT_FILENAME = program_constants.ScriptRun.SCRIPT_FILENAME  # Default filename for the script file
    # I start reading the file
    file = open(SCRIPT_FILENAME, "r")
    line = file.readline()  # I skip the first line, that was the program mode
    line = file.readline()  # I take the second line, that was the input filename
    # I take the piece of the string after the : symbol and I strip it
    filename = line.split(":")[1].strip()
    file.close()
    return filename
#.................................................

def retrieve_settings():
    """This function retrieves the settings filename
    from the script.pfs file.

    Returns:
        settings_filename (string): the settings filename
    """
    # Constants:
    program_constants = ProgramConstants()
    FILENAME = program_constants.ScriptRun.SCRIPT_FILENAME  # Default filename for the script file
    # I start reading the file
    file = open(FILENAME, "r")
    line = file.readline()  # I skip the first line, that was the program mode
    line = file.readline()  # I skip the second line, that was the input filename
    line = file.readline()  # I take the third line, that was the settings filename
    # I take the piece of the string after the : symbol and I strip it
    settings_filename = line.split(":")[1].strip()
    file.close()
    return settings_filename
#.................................................
#   Possible improvements:
#   -More customization options and error handling.
#.................................................
#   KNOW PROBLEMS:
#   -None
#.................................................