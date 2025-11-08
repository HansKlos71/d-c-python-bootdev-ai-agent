import os
from google.genai import types


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