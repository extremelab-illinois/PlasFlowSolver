#.................................................
#   WRITE_OUTPUT.PY, v2.0.0, December 2024, Domenico Lanza.
#.................................................
#   This module is needed to write the output file.
#.................................................
import IO_operations.write_output_srun as write_output_srun_file  # Module to write the output file in a .srun run
import IO_operations.write_output_xlsx as write_output_xlsx_file  # Module to write the output file in a .xlsx run
import IO_operations.write_output_filerun as write_output_filerun_file  # Module to write the output file in a .in run
from utils.exit_program import exit_program  # Module to exit the program

def write_output(output_filename, out_object, program_mode, df_object):
    if program_mode == 1:  # Single run
        write_output_srun_file.write_output_srun(output_filename, out_object)
    elif program_mode == 2:  # xlsx run
        write_output_xlsx_file.write_output_xlsx(output_filename, out_object)
    elif program_mode == 3:  # File run
        write_output_filerun_file.write_output_filerun(df_object, output_filename, out_object)
    else:
        print("ERROR: Invalid program mode. You should never see this message...")
        print("The program will now terminate.")
        exit_program()
#.................................................
#   Possible improvements:
#   - Better structure for functions inputs.
#.................................................
#   Known problems:
#   None.
#.................................................