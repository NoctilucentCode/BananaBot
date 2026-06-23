### Import Libraries ###
import os
import subprocess
from google import genai
from google.genai import types


### Define the schema used with Gemini API ###
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file in the specified directory with given arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the specified directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING
                ),
                description="Arguments to pass to the Python file",
            ),
        },
    ),
)


### Python File Execution Function ###
def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        target_directory_absolute = os.path.abspath(working_directory)
        target_file_absolute = os.path.normpath(os.path.join(target_directory_absolute, file_path))
        valid_target_file = os.path.commonpath([target_directory_absolute, target_file_absolute]) == target_directory_absolute
        if not valid_target_file:
            return(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
        if not os.path.isfile(target_file_absolute):
            return(f'Error: "{file_path}" does not exist or is not a regular file')
        if file_name := os.path.basename(target_file_absolute):
            if not file_name.endswith('.py'):
                return(f'Error: "{file_path}" is not a Python file')
        result = subprocess.run(cwd=target_directory_absolute, args=['python', target_file_absolute] + (args if args else []), capture_output=True, text=True, timeout=30)
        output = []
        # append exit code message if needed
        if result.returncode != 0:
            output.append(f'Process exited with code {result.returncode}')
        # append "No output produced" if needed
        if result.stdout.strip() == "" and result.stderr.strip() == "":
                output.append(f"No output produced")
        # append stdout if present
        if result.stdout.strip():
                output.append(f"STDOUT:\n{result.stdout}")
        # append stderr if present
        if result.stderr.strip():
                output.append(f"STDERR:\n{result.stderr}")
        
        return "\n".join(output)
    except Exception as e:
        return(f"Error: executing Python file: {e}")