### Import Libraries ###
import os
from google import genai
from google.genai import types
config_limit = 10000  # Maximum number of characters to read from a file


### Define the schema used with Gemini API ###
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Retrieves the content of a specified file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to list files from, relative to the working directory",
            ),
        },
    ),
)


### File Content Function ###
def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        target_directory_absolute = os.path.abspath(working_directory)
        target_file_absolute = os.path.normpath(os.path.join(target_directory_absolute, file_path))
        valid_target_file = os.path.commonpath([target_directory_absolute, target_file_absolute]) == target_directory_absolute
        if not valid_target_file:
            return(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
        if not os.path.isfile(target_file_absolute):
            return(f'Error: File not found or is not a regular file: "{file_path}"')
        with open(target_file_absolute, 'r') as f:
            content = f.read(config_limit)  # Read up to the configured limit characters
            if f.read(1):  # Check if there's more content beyond the limit
                content += f"\n[...File \"{file_path}\" truncated at {config_limit} characters]"
        return content
    except Exception as e:
        return(f'Error: {str(e)}')