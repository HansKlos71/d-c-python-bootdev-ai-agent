import os
from google.genai import types

def write_file(working_directory, file_path, content):
    absolute_path = os.path.abspath(os.path.join(working_directory, file_path))
    absolute_working_directory = os.path.abspath(working_directory)

    if not absolute_path.startswith(absolute_working_directory):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(absolute_working_directory):
        try:
            os.makedirs(absolute_working_directory)
        except Exception as e:
            return f"Error: Failed to create directories for {file_path}: {str(e)}"
    try:
        with open(absolute_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: Failed to write to {file_path}: {str(e)}"
    

scheme_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            'file_path': types.Schema(
                type=types.Type.STRING,
                description ="The path to the file to write to, relative to the working directory.",
            ),
            'content': types.Schema(
                type=types.Type.STRING,
                description="The content to write into the file.",
            )
        }
    )
)