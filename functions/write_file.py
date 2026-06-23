### Import Libraries ###
import os
from google import genai
from google.genai import types


### Define the schema used with Gemini API ###
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specified file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to write the file to, relative to the working directory (default is the working directory itself)",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the specified directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
    ),
)


### File Writing Function ###
def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        target_directory_absolute = os.path.abspath(working_directory)
        target_file_absolute = os.path.normpath(os.path.join(target_directory_absolute, file_path))
        valid_target_file = os.path.commonpath([target_directory_absolute, target_file_absolute]) == target_directory_absolute
        if not valid_target_file:
            return(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
        target_dir = os.path.dirname(target_file_absolute)
        if os.path.exists(target_file_absolute) and os.path.isdir(target_file_absolute):
            return(f'Error: Cannot write to "{file_path}" as it is a directory')
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        with open(target_file_absolute, 'w') as f:
            f.write(content)
        return(f'Successfully wrote to "{file_path}" ({len(content)} characters written)')
    except Exception as e:
        return(f'Error: {str(e)}')