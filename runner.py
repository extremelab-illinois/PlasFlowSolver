"""
@file runner.py

@brief Convenience script to run main.py on multiple XLSX cases.

Copyright (C) 2023-2025 The Board of Trustees of the University of Illinois.
All rights reserved.

This file is part of PlasFlowSolver: a data reduction model for ICP wind tunnels.

PlasFlowSolver is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

PlasFlowSolver is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with PlasFlowSolver.  If not, see 
<http://www.gnu.org/licenses/>.
"""

# This is not a project file, but a script that can be used to run the main.py script on multiple xlsx files

import subprocess  # For running python scripts from python

def runner(xlsx_to_run):
    """Run the main.py script for each xlsx file in the list

    Args:
        xlsx_to_run (list): List of xlsx files to run the main.py script on
    """
    for xlsx in xlsx_to_run:  # Select each xlsx file in the list
        print("Running file: ", xlsx)
        # Create a bash.pfs file to run PlasFlowSolver
        f = open("script.pfs", "w")
        f.write("Mode: xlsx\n")
        f.write("File: " + xlsx + "\n")
        f.write("Settings: NA\n")
        f.close()
        # Run the main.py script
        cmd = ['python3', 'main.py']
        subprocess.Popen(cmd).wait()  # Wait for the process to finish
        print("Finished running file: ", xlsx)

# Example usage:
xlsx_to_run = ["example_xlsx.xlsx", "example_xlsx2.xlsx"]
runner(xlsx_to_run)
