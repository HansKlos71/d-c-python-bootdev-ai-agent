from .get_files_info import scheme_get_files_info
from google.genai import types

available_functions = types.Tool(
    function_declarations=[
        scheme_get_files_info,
    ]
)