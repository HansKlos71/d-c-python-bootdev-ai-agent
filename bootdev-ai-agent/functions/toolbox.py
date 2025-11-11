import os
from config import MAX_CHARS
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


def run_python_file(working_directory, file_path, args=[]):
    absolute_working_directory = os.path.abspath(working_directory)
    absolute_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not absolute_path.startswith(absolute_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(absolute_path):
        return f'Error: File "{file_path}" not found.'
    if not absolute_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    import subprocess
    
    try:
        complete_process = subprocess.run(["python3", absolute_path] + args, capture_output=True, timeout=30)
        print(f"STDOUT:\n{complete_process.stdout.decode()}")
        print(f"STDERR:\n{complete_process.stderr.decode()}")

        if complete_process.returncode != 0:
            print(f"Error: PRocess exited with code X")
        if complete_process.stdout.strip() == None:
            print("No output produced.")
    except Exception as e:
        return f"Error: executing Python file: {e}"
    

scheme_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file located within the working directory and returns its output.",
    parameters = types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="A list of string arguments to pass to the Python file when executing it.",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="A string argument to pass to the Python file."
                )
            )
        }
    )
)


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


def get_file_content(working_directory, file_path, max_chars=MAX_CHARS):

    absolute_working_directory = os.path.abspath(working_directory)
    absolute_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not absolute_path.startswith(absolute_working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(absolute_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    with open(absolute_path, "r") as f:
        content = f.read()
        if len(content) > max_chars:
            content = content[:max_chars] + f"[...File {file_path} truncated at {max_chars} characters]"
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