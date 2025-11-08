import os


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