#.................................................
#   READ_DATA.PY, v2.0.0, December 2024, Domenico Lanza.
#.................................................
#   This module is needed to read the
#   data and create the the dataframe object.
#.................................................

from IO_operations.read_srun import read_srun  # Function to read the .srun file
from IO_operations.read_xlsx import read_xlsx  # Function to read the .xlsx file
from IO_operations.read_filerun import read_filerun  # Function to read the .in and .pfs files

def read_data(program_mode, script_run):
    """This function reads the data from the input files
    and creates the dataframe object.

    Args:
        program_mode (int): the program mode (1, 2 or 3)
        script_run (boolean): the script run flag

    Raises:
        Exception: if an error occurs while reading the input files

    Returns:
        df_object (dataframe_class): the dataframe object
        output_filename (string): the output filename
    """
    # Check the program mode:
    if (program_mode == 1):  # Single run
        print("Mode selected: Single run.")
        # In this case, I want to read a .srun file, with only 1 case
        try:
            df_object, output_filename = read_srun(script_run)
        except Exception as e:
            raise Exception("Error while reading the .srun file: " + str(e) + "\n Please check your .srun file format and try again.")
    elif (program_mode == 2):  # xlsx run
        print("Mode selected: xlsx run.")
        # In this case, I want to read an xlsx file with multiple cases
        try:
            df_object, output_filename = read_xlsx(script_run)
        except Exception as e:
            raise Exception("Error while reading the xlsx file: " + str(e) + "\n Please check your .xlsx file format and try again.")
    elif (program_mode == 3):  # File run
        print("Mode selected: .in and .pfs file run.")
        try:
            df_object, output_filename = read_filerun(script_run)
        except Exception as e:
            raise Exception("Error while reading the .in and .pfs files: " + str(e) + "\n Please check your .in and .pfs files format and try again.")
    else:
        raise Exception("ERROR: Invalid program mode (you shouln't be able to see this message. Please check your retrieve_program_mode function.)")
    
    return df_object, output_filename
#.................................................
#   Possible improvements:
#   - More specific exceptions
#   - More program modes
#.................................................
#   KNOW PROBLEMS:
#   -None
#.................................................
    