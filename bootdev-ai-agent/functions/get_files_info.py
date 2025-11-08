import os
from google.genai import types


def get_files_info(working_directory, directory="."):
    # directory param is a relative path whitin the working_directory
    
    absolute_working_directory = os.path.abspath(working_directory)
    absolute_path = os.path.abspath(os.path.join(working_directory, directory))

    if not absolute_path.startswith(absolute_working_directory):
        return f"Error: Cannot list {directory} as it is outside the working directory."
    if not os.path.isdir(absolute_path):
        return f"Error: {directory} is not a directory."
    
    files = os.listdir(absolute_path)
    file_info_list = ""
    
    for file in files:
        file_info_list += f"- {file}: file_size={os.path.getsize(os.path.join(absolute_path, file))} bytes, is_dir={os.path.isdir(os.path.join(absolute_path, file))}\n"
    
    return file_info_list

scheme_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            )
        }
    )
)    