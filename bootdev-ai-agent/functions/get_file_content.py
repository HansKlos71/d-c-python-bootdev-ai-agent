import os
from config import MAX_CHARS

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