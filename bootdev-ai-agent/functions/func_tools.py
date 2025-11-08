from .get_files_info import scheme_get_files_info
from .get_file_content import scheme_get_file_content
from .run_python_files import scheme_run_python_file
from .write_file import scheme_write_file
from google.genai import types

available_functions = types.Tool(
    function_declarations=[
        scheme_get_files_info,
        scheme_get_file_content,
        scheme_run_python_file,
        scheme_write_file,
    ]
)