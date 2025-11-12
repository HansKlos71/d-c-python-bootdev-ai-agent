from google.genai import types
from config import WORKING_DIR
from .toolbox import (
    GetFilesInfoTool,
    GetFileContentTool,
    RunPythonFileTool,
    WriteFileTool,
)


class ToolMapper:
    def __init__(self):
        self.__tools = {
            "get_files_info": GetFilesInfoTool(),
            "get_file_content": GetFileContentTool(),
            "run_python_file": RunPythonFileTool(),
            "write_file": WriteFileTool(),
        }
        self.__tool_schemas_map =[
            tool.get_schema() for tool in self.__tools.values()
        ]
    
    def get_available_function_map(self):
        return self.__tools

    def get_available_function_schemas(self):
        return self.__tool_schemas_map


class FunctionMapper(ToolMapper):
    pass


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
        print("calling!")
        print(f" - with args: {args}")
        function_result = function_map[function_name].call(**args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ]
        )