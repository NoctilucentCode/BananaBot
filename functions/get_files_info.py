### Import necessary libraries ###
import os



### File Information Function ###
def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        target_directory_absolute = os.path.abspath(working_directory)
        target_directory = os.path.normpath(os.path.join(target_directory_absolute, directory))
        # Will be True or False
        valid_target_dir = os.path.commonpath([target_directory_absolute, target_directory]) == target_directory_absolute
        if not valid_target_dir:
            return(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        if directory is not None and not os.path.isdir(target_directory):
            return(f'Error: "{directory}" is not a directory')
        else:
            file_lines = []
            for file in os.listdir(target_directory):
                file_path = os.path.join(target_directory, file)
                is_dir = os.path.isdir(file_path)
                file_size = os.path.getsize(file_path)
                file_lines.append(f"  - {file}: file_size={file_size} bytes, is_dir={is_dir}")
            return '\n'.join(file_lines)

    except Exception as e:
        return(f'Error: {str(e)}')