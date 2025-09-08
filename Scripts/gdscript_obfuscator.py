import os
import shutil
import random
import string
import re
import time


def copy_folder_structure(source_folder, destination_folder):
    #Copy the folder structure from source to destination without copying files.
    parent_folder = os.path.dirname(source_folder)

    # Create the destination directory if it doesn't exist
    os.makedirs(destination_folder, exist_ok=True)

    # Walk through the source directory
    for folder, subfolderNames, file in os.walk(source_folder):
        subfolderNames[:] = [subfolder for subfolder in subfolderNames if subfolder not in [".git", ".godot"]] # Exclude folder exclusion
        subfolder_name = os.path.relpath(folder, source_folder) # Calculate the relative path from the source directory
        destination_directory = os.path.join(destination_folder, subfolder_name) # Create the corresponding directory in the destination
        os.makedirs(destination_directory, exist_ok=True)

def increment_if_exists(file_path):
    #If the file already exists, increment the filename by adding a number at the end
    base, extension = os.path.splitext(file_path)
    if not os.path.exists(file_path): 
        new_file_path = file_path
    else:
        counter = 1
        os.rename(file_path, f"{base}_{counter}{extension}")
        new_file_path = file_path

        while os.path.exists(new_file_path):
            counter += 1
            new_file_path = f"{base}_{counter}{extension}"

    return new_file_path
    

def obfuscate_name(length):
    """Generate a random obfuscated name of specified length."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def obfuscate_gdscript(file_path, overwrite, name_length, main_folder, structure_namemaps=False, namemaps_folder_path=""):
    with open(file_path, 'r') as file:
        source = file.read()

    # Remove comments
    source = re.sub(r'#.*?$', '', source, flags=re.MULTILINE)  # Remove single-line comments
    source = re.sub(r'/\*.*?\*/', '', source, flags=re.DOTALL)  # Remove multi-line comments

    # Dictionary to store original names and their obfuscated counterparts
    name_map = {}

    # Regex patterns for variables, functions, classes, constants, and instances
    constant_pattern = r'\bconst\s+(\w+)'  # Matches constant declarations
    variable_pattern = r'\bvar\s+(\w+)'  # Matches variable declarations
    function_pattern = r'\bfunc\s+(\w+)'  # Matches function definitions
    # class_pattern = r'\bclass\s+(\w+)'    # Matches class definitions
    # extends_pattern = r'\bextends\s+(\w+)'  # Matches class inheritance
    type_pattern = r'\btype\s+(\w+)'  # Matches type aliases

    # Function to replace names in the source code
    def replace_names(match):
        original_name = match.group(1)
        if original_name in ["_ready", "_process"]: return match.group(0)  # Skip obfuscation for important functions and Return the original match without changes
        if original_name not in name_map:
            obfuscated_name = obfuscate_name(name_length)
            name_map[original_name] = obfuscated_name
        return f"{match.group(0).replace(original_name, name_map[original_name])}"

    # Replace names in the source code
    source = re.sub(constant_pattern, replace_names, source)
    source = re.sub(variable_pattern, replace_names, source)
    source = re.sub(function_pattern, replace_names, source)
    # source = re.sub(class_pattern, replace_names, source)
    # source = re.sub(extends_pattern, replace_names, source)
    source = re.sub(type_pattern, replace_names, source)

    # Replace instances of names throughout the code
    for original, obfuscated in name_map.items(): source = re.sub(r'\b' + re.escape(original) + r'\b', obfuscated, source)

    # Determine output file path
    if overwrite: output_file_path = file_path
    else: output_file_path = file_path.replace('.gd', '_obfuscated.gd')

    # Write the obfuscated code back to the specified file
    with open(output_file_path, 'w') as file: file.write(source)

    # Write the name mapping to a separate file
    if os.path.isdir(main_folder):
        main_folder = os.path.normpath(main_folder)
        file_path = os.path.normpath(file_path)
        relative_path = os.path.relpath(file_path, main_folder)

        # Create the corresponding directory in the namemaps folder
        if structure_namemaps: namemaps_folder_path = os.path.join(namemaps_folder_path, relative_path)
        else: namemaps_folder_path = os.path.join(namemaps_folder_path, os.path.basename(file_path))
        # Write the name mapping to a separate file
        mapping_file_path = increment_if_exists(namemaps_folder_path.replace('.gd', '_name_map.txt'))
        with open(mapping_file_path, 'w') as file:
            for original, obfuscated in name_map.items():
                file.write(f"{original} -> {obfuscated}\n")
    else:
        mapping_file_path = file_path.replace('.gd', '_name_map.txt')
        with open(mapping_file_path, 'w') as file:
            for original, obfuscated in name_map.items():
                file.write(f"{original} -> {obfuscated}\n")

def main():
    input_path = input("Enter the file path or directory containing GDScript files: ")
    overwrite = input("Do you want to overwrite the original files? (yes/no): ").strip().lower() == 'yes'
    name_length = int(input("Enter the desired length for generated names: "))
    #Check if name_length is a number
    while not isinstance(name_length, int) or name_length <= 0:
        print("Please enter a valid positive integer for name length.")
        name_length = int(input("Enter the desired length for generated names: "))

    # Check if the input is a directory or a file
    if os.path.isfile(input_path) and input_path.endswith('.gd') and not input_path.endswith('_obfuscated.gd'):
        print(f"Obfuscating {input_path}...")
        obfuscate_gdscript(input_path, overwrite, name_length)
        print(f"Obfuscation successful. Mapping file created.")
    elif os.path.isdir(input_path):
        folder_path = os.path.abspath(input_path)
        folder_name = os.path.basename(folder_path)
        folder_parent_dir = os.path.dirname(folder_path)
        #Duplicate and rename the the original folder
        if not overwrite:
            # Create the new folder path for obfuscation
            obfuscated_folder_name = os.path.basename(folder_path) + '_obfuscated'
            obfuscated_folder_path = os.path.join(folder_parent_dir, obfuscated_folder_name)

            # Copy the source folder to the new folder path and obfuscate the copy
            if os.path.exists(obfuscated_folder_path):
                overwrite_ob = input(f"There is already a folder called {obfuscated_folder_name}. Do you want to overwrite it? (yes/no): ").strip().lower() == 'yes'
                if overwrite_ob:
                    shutil.rmtree(obfuscated_folder_path)
                    shutil.copytree(input_path, obfuscated_folder_path)
                    print(f"Obfuscating source code in {folder_name} as {obfuscated_folder_name}...")
                else:
                    print("Terminating operation...")
                    time.sleep(1)
                    print("Operation terminated.")
                    return
            else: shutil.copytree(input_path, obfuscated_folder_path)
            input_path = obfuscated_folder_path
            overwrite = True
            
        structure_namemaps = input(f"Do you want to copy the folder structure of \"{folder_name}\" for the name map files? (yes/no): ").strip().lower() == 'yes'
        namemaps_folder_path = folder_path + '_name_maps'
        if structure_namemaps: copy_folder_structure(input_path, namemaps_folder_path)
        else: os.makedirs(namemaps_folder_path, exist_ok=True)
            
        # Walk through the directory
        for folder, subfolderNames, files in os.walk(input_path):
            for filename in files:
                # Check if the file has a .gd extension
                if filename.endswith('.gd') and not filename.endswith('_obfuscated.gd'):
                    file_path = os.path.join(folder, filename)
                    print(f"Obfuscating {filename}...")
                    obfuscate_gdscript(file_path, overwrite, name_length, input_path, structure_namemaps, os.path.abspath(namemaps_folder_path))
                    print(f"Obfuscation successful. Mapping file created.")
    else:
        print("The specified path is not valid. Please enter a valid directory or a .gd file.")

if __name__ == "__main__":
    print("GDScript Code Obfuscator")
    print("------------------------\n")
    main()
