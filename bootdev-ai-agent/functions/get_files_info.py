import os


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


def get_file_content(working_directory, file_path):

    absolute_working_directory = os.path.abspath(working_directory)
    absolute_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not absolute_path.startswith(absolute_working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(absolute_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    MAX_CHARS = 10000

    with open(absolute_path, "r") as f:
        content = f.read()
        if len(content) > MAX_CHARS:
            content = content[:MAX_CHARS] + f"[...File {file_path} truncated at 10000 characters]"
    return content


def write_file(working_directory, file_path, content):
    absolute_working_directory = os.path.abspath(working_directory)
    absolute_path = os.path.abspath(os.path.join(working_directory, file_path))

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
    