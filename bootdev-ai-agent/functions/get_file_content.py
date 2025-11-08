import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):

    absolute_working_directory = os.path.abspath(working_directory)
    absolute_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not absolute_path.startswith(absolute_working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(absolute_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    with open(absolute_path, "r") as f:
        content = f.read()
        if len(content) > MAX_CHARS:
            content = content[:MAX_CHARS] + f"[...File {file_path} truncated at {MAX_CHARS} characters]"
    return content

scheme_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Retrieves the content of a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory.",
            )
        }
    )
)