### Import Library ###
import os
from collections.abc import Callable
from google import genai
from google.genai import types
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import schema_write_file, write_file
from functions.get_file_content import get_file_content, schema_get_file_content

### Other Constants ###

function_map: dict[str, Callable[..., str]] = {
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
    "get_files_info": get_files_info}


### Functions Library ###
available_functions = types.Tool(function_declarations=[schema_get_files_info, schema_run_python_file, schema_write_file, schema_get_file_content],)

def call_function(function_call: types.FunctionCall, verbose: bool = False) -> types.Content:
    if verbose:
        print(f" - Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")
    function_name = function_call.name or ""
    if function_name not in function_map:
        return types.Content( role="tool", parts=[
types.Part.from_function_response(
            name=function_name,
            response={"error": f"Unknown function: {function_name}"},
        )
    ],
)
    else:
        args = dict(function_call.args) if function_call.args else {}
        args["working_directory"] = "./calculator"
        result = function_map[function_name](**args)
        
        return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"result": result},
        )
    ],
)