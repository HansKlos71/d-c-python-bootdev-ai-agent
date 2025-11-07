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