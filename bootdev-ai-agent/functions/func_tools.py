from .get_files_info import scheme_get_files_info, get_files_info
from .get_file_content import scheme_get_file_content, get_file_content
from .run_python_files import scheme_run_python_file, run_python_file
from .write_file import scheme_write_file, write_file
from google.genai import types
from config import WORKING_DIR

class FunctionMapper:
    def __init__(self):
        self.__function_map = {
            "get_files_info": get_files_info,
            "get_file_content": get_file_content,
            "run_python_file": run_python_file,
            "write_file": write_file,
        }
        self.__function_schemas_map =[
            scheme_get_files_info,
            scheme_get_file_content,
            scheme_run_python_file,
            scheme_write_file,
        ]
    
    def get_available_function_map(self):
        return self.__function_map

    def get_available_function_schemas(self):
        return self.__function_schemas_map


class FunctionCaller:
    def __init__(self, verbose=False, function_mapper: FunctionMapper = FunctionMapper()):
        self.verbose = verbose
        self.__available_function_map = function_mapper.get_available_function_map()

    def call_function(self, function_call_part):   
        if self.verbose:
            print(f" - Calling function: {function_call_part.name}({function_call_part.args})")
        else:
            print(f" - Calling function: {function_call_part.name}")

        function_map = self.__available_function_map
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