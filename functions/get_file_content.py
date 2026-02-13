import os
from dotenv import load_dotenv
from google.genai import types

load_dotenv()
MAX_CHAR = os.environ.get("MAX_CHAR")

def get_file_content(working_directory, file_path):
    abs_path = os.path.abspath(working_directory)
    full_path = os.path.normpath(os.path.join(abs_path, file_path))
    valid_target_dir = os.path.commonpath([abs_path, full_path]) == abs_path
    if valid_target_dir:
        if os.path.isfile(full_path):
            try:
                open_file = open(full_path)
                return open_file.read(int(MAX_CHAR))
            except Exception as err:
                return f"Error: {err}"
        else:
            return f'Error: File not found or is not a regular file: "{file_path}"'
    else:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Return the contents of a specified file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file.",
            ),
        },
    required=["file_path"],
    ),
)