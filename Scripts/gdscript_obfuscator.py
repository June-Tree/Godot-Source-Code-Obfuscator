import os
import subprocess
import shutil
import random
import string
import json
import re
import time


def obfuscate_name(length):
    return "".join(random.choices(string.ascii_letters + string.digits, k=length)) #Generate a random obfuscated name of specified length.

def obfuscate_gdscript(file_path, overwrite, name_length, input_path, relative_path):
    # Determine output file path
    if overwrite: output_file_path = file_path
    else: output_file_path = file_path.replace(".gd", "_obfuscated.gd")
    
    if os.path.isfile(input_path): file_name = os.path.basename(file_path)
    else: file_name = relative_path
    
    obfuscation_data = {
        file_name: {
            "name_map": {
                "const": {},
                "var": {},
                "func": {},
                "class_name": {}
            },
            "comments": {}
        }
    }

    identifiers = []
    obfuscated_code = []

    #Collect data from the .gd file.
    with open(file_path, 'r') as file: lines = file.readlines()
    
    for line_number, line in enumerate(lines):
        #Process comments
        comment_match = re.search(r'#.*$', line)
        if comment_match:
            comment = comment_match.group(0).strip() # Get the entire comment
            comment_start = comment_match.start(0)  # Get the start position of the comment
            obfuscation_data[file_name]["comments"][comment] = {
                "line_number": line_number+1,
                "starting_index": comment_start
            } # Store the comment with details on its exact location
        
        # Obfuscate identifiers
        def replace_names(keyword, match):
            name_map = obfuscation_data[file_name]["name_map"]
            identifier = match.group(1)
            if identifier in ["_ready", "_process"]: return identifier, identifier # Skip obfuscation for important functions and return the original match without changes
            if identifier not in name_map[keyword]:
                obfuscated_name = obfuscate_name(name_length)
                name_map[keyword][identifier] = obfuscated_name
                return identifier, obfuscated_name
            
        
        for keyword in obfuscation_data[file_name]["name_map"]:
            if keyword == "class_name": pass
            else:
                pattern = re.compile(rf'^\s*\b{re.escape(keyword)}\b\s+([^:\W]+)')  # General match for identifiers
                match = pattern.search(line)
                if match:
                    identifier, obfuscated_name = replace_names(keyword, match)
                    identifiers.append(identifier)
                else: identifier = None

        # Obfuscate class names
        class_pattern = re.compile(r'class_name\s+(\w+)')
        class_match = class_pattern.search(line)
        if class_match:
            original_class_name = class_match.group(1)
            class_dict = obfuscation_data[file_name]["name_map"]["class_name"]
            if original_class_name not in class_dict:
                obfuscated_class_name = obfuscate_name(name_length)
                class_dict[original_class_name] = [
                    obfuscated_class_name,
                    []  # Placeholder for referencing files
                ]
                line = line.replace(original_class_name, obfuscated_class_name)

    for line_number, line in enumerate(lines):
        for comment, details in obfuscation_data[file_name]["comments"].items():
            if line_number + 1 == details["line_number"]: 
                line = line.replace(comment, "")
        for identifier in identifiers:
            for keyword in obfuscation_data[file_name]["name_map"].values():
                if identifier in keyword.keys():
                    obfuscated_name = keyword[identifier]
                    line = line.replace(identifier, obfuscated_name)
        obfuscated_code.append(line)
    with open(output_file_path, 'w') as file: file.writelines(obfuscated_code)

    # Obfuscation data cleanup
        # Remove abscent keywords
    abscent_keywords = []
    name_map = obfuscation_data[file_name]["name_map"]
    for keyword, value in name_map.items(): #delete 
        if name_map[keyword] == {}: abscent_keywords.append(keyword)
    for keyword in abscent_keywords:
        del obfuscation_data[file_name]["name_map"][keyword]
        # Remove comments dictionary if empty
    if obfuscation_data[file_name]["comments"] == {}: del obfuscation_data[file_name]["comments"]

    return obfuscation_data

def main():
    input_path = input("Enter a file path or directory containing GDScript files: ")
    # Cleanup input
    input_path = input_path.replace("'", "") # Remove single quotes
    input_path = input_path.replace('"', "") # Remove double quotes

    overwrite = input("Do you want to overwrite the file provided? (yes/no): ").strip().lower() == "yes"
    
    name_length = int(input("Enter the desired length for generated names: "))
    while not isinstance(name_length, int) or name_length <= 0: #Check if name_length is a positive number
        print("Please enter a valid positive integer for name length.")
        name_length = int(input("Enter the desired length for generated names: "))

    all_obfuscation_data = {}
    # Check if the input is a directory or a file
    if os.path.isfile(input_path) and input_path.endswith(".gd") and not input_path.endswith("_obfuscated.gd"):
        print(f"Obfuscating \"{input_path}\"...")
        mapping_file = input_path.replace(".gd", "_obfuscation_data.json")
        obfuscation_data = obfuscate_gdscript(input_path, overwrite, name_length, input_path, os.path.basename(input_path))
        all_obfuscation_data.update(obfuscation_data)
        print(f"Code obfuscation successful. Mapping file created.")
    elif os.path.isdir(input_path):
        folder_path = os.path.abspath(input_path)
        folder_name = os.path.basename(folder_path)
        folder_parent_dir = os.path.dirname(folder_path)
        mapping_file = folder_path + "_obfuscation_data.json"
        #Duplicate and rename the the original folder
        if not overwrite:
            # Create the new folder path for obfuscation
            obfuscated_folder_name = os.path.basename(folder_path) + "_obfuscated"
            obfuscated_folder_path = os.path.join(folder_parent_dir, obfuscated_folder_name)

            # Copy the source folder to the new folder path and obfuscate the copy
            if os.path.exists(obfuscated_folder_path):
                overwrite_ob = input(f"There is already a folder called \"{obfuscated_folder_name}\". Do you want to overwrite it? (yes/no): ").strip().lower() == "yes"
                if overwrite_ob:
                    shutil.rmtree(obfuscated_folder_path)
                    shutil.copytree(input_path, obfuscated_folder_path)
                    print(f"Obfuscating source code in \"{folder_name}\" as \"{obfuscated_folder_name}\"...")
                else:
                    print("Terminating operation...")
                    time.sleep(1)
                    print("Operation terminated.")
                    return
            else: shutil.copytree(input_path, obfuscated_folder_path)
            input_path = obfuscated_folder_path
            overwrite = True
        
        print(f"Creating code map...")
        # Walk through the directory
        for folder, subfolderNames, files in os.walk(input_path):
            # Remove repository data
            if ".git" in subfolderNames:
                remove_vc = input(f"Would you like to remove version control? (yes/no): ").strip().lower() == "yes"
                if remove_vc:
                    git_folder = os.path.join(folder, ".git")
                    # Forcefully delete the .git directory using system command
                    if os.name == "nt":  # For Windows
                        subprocess.run(['rmdir', '/s', '/q', git_folder], check=True, shell=True)
                    else:  # For Linux or macOS
                        subprocess.run(['rm', '-rf', git_folder], check=True)
                    print(f"Version control removed.")
            for file in files:
                # Check if the file has a .gd extension
                if file.endswith(".gd") and not file.endswith("_obfuscated.gd"):
                    file_path = os.path.join(folder, file)
                    objective_file_path = file_path.replace("_obfuscated", "")
                    relative_path = os.path.relpath(objective_file_path, mapping_file)[3:]
                    print(f"Obfuscating \"{file}\"...")
                    obfuscation_data = obfuscate_gdscript(file_path, overwrite, name_length, input_path, relative_path)
                    all_obfuscation_data.update(obfuscation_data)
                    print(f"Obfuscation successful. Mapping details updated.")
        print(f"Code obfuscation successful.")
    else:
        return print("The specified path is not valid. Please enter a valid directory or a .gd file.")
    if mapping_file: 
        with open(mapping_file, 'w') as json_file: json.dump(all_obfuscation_data, json_file, indent=4)

if __name__ == '__main__':
    print("GDScript Code Obfuscator")
    print("------------------------\n")
    main()
