import os, time, subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    abs_path = os.path.abspath(working_directory)
    full_path = os.path.normpath(os.path.join(abs_path, file_path))
    valid_target_dir = os.path.commonpath([abs_path, full_path]) == abs_path
    if valid_target_dir:
        if os.path.isfile(full_path) == False:
            return f'Error: "{file_path}" does not exist or is not a regular file'
        else:
            if full_path.endswith(".py"):
                try:
                    command = ["python", full_path]

                    if args != None:
                        command.extend(args)
                    run_command = subprocess.run(command, text=True, capture_output=True)

                    string_to_return = ""

                    if run_command.returncode != 0:
                        string_to_return = string_to_return + f"Process exited with code {run_command.returncode}\n"

                    if len(run_command.stdout) != 0 or len(run_command.stderr) != 0:
                        string_to_return = string_to_return + f"STDOUT: {run_command.stdout}\nSTDERR: {run_command.stderr}"
                    time.sleep(30)
                    return string_to_return

                except Exception as err:
                    return f"Error: {err}"
            else:
                return f'Error: "{file_path}" is not a Python file'
            
    else:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a specified Python file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file.",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="Arguments to pass, optional.",
            ),
        },
    required=["file_path"],
    ),
)