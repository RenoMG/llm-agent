import os
from google.genai import types

def write_file(working_directory, file_path, content):
    abs_path = os.path.abspath(working_directory)
    full_path = os.path.normpath(os.path.join(abs_path, file_path))
    valid_target_dir = os.path.commonpath([abs_path, full_path]) == abs_path
    if valid_target_dir:
        if os.path.isfile(full_path) == False:
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        else:
            try:
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, "w") as f:
                    f.write(content)
            except Exception as err:
                return f"Error: {err}"
            
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    else:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write content to a specified file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file.",
            ),
        },
    required=["file_path", "content"],
    ),
)