from .get_files_info import scheme_get_files_info, get_files_info
from .get_file_content import scheme_get_file_content, get_file_content
from .run_python_files import scheme_run_python_file, run_python_file
from .write_file import scheme_write_file, write_file
from google.genai import types
from config import WORKING_DIR

available_functions = types.Tool(
    function_declarations=[
        scheme_get_files_info,
        scheme_get_file_content,
        scheme_run_python_file,
        scheme_write_file,
    ]
)

def call_function(function_call_part, verbose=False):   
    if verbose:
        print(f" - Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    function_name = function_call_part.name

    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    args = dict(function_call_part.args)
    args["working_directory"] = WORKING_DIR
    function_result = function_map[function_name](**args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ]
    )