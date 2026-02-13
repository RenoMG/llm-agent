import os

def get_files_info(working_directory, directory="."):
    abs_path = os.path.abspath(working_directory)
    full_path = os.path.normpath(os.path.join(abs_path, directory))
    if os.path.isdir(full_path):
        valid_target_dir = os.path.commonpath([abs_path, full_path]) == abs_path

        if valid_target_dir:
            get_files = os.listdir(full_path)

            file_info = []
            for f in get_files:
                try:
                    file_info.append(f"- {f}: file_size={os.path.getsize(f"{full_path}/{f}")} bytes, is_dir={os.path.isdir(f)}\n")
                except Exception as err:
                    return f"Error: {err}"

            print("".join(file_info))
        else:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    else:
        f'Error: "{directory}" is not a directory'

get_files_info("/home/ubuntu/workspace/bootdotdev/llm-agent", "calculator")