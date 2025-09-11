import os
import shutil
import json
import time


def remove_suffix(name, suffix):
    if name.endswith(suffix):
        return name[:-len(suffix)]
    return name

def check_for_obfuscation_suffixes(file_path):
    #Create a variable that has (forcefully) has the obfuscated suffix
    suffixes = ["_obfuscated.gd", ".gd"]
    # Check and remove the suffix to get the base name
    for suffix in suffixes:
        if file_path.endswith(suffix):
            # Remove the suffix and return the base name + obfuscated suffix
            filename_ob = file_path[:-len(suffix)] + "_obfuscated.gd"
            mapping_file = file_path[:-len(suffix)] + "_obfuscation_data.json"
            break
    
    # folder = os.listdir(file_path)
    folder = file_path.rsplit("/", 1)[0]
    if file_path.endswith("_obfuscated.gd"):
        return file_path, filename_ob, mapping_file
    else: #Look for a duplicate with the obfuscated suffix
      for file in folder:
        if file.endswith("_obfuscated.gd") and remove_suffix(file, "_obfuscated.gd") == remove_suffix(file_path, ".gd"): #Compare files
          obfuscated_file = os.path.join(folder, file)
          return obfuscated_file, filename_ob, mapping_file
      #Then either the original file was overwritten, or no obfuscated version exists
      return file_path, filename_ob, mapping_file

def restore_gdscript(obfuscated_file_path, mapping_file_path, overwrite, isDirectory, relative_path):
    # Determine output file path
    if not isDirectory:
        if overwrite: output_file_path = obfuscated_file_path.replace("_obfuscated.gd", ".gd")
        else:
            if obfuscated_file_path.endswith("_obfuscated.gd") : output_file_path = obfuscated_file_path.replace("_obfuscated.gd", "_restored.gd")
            else: output_file_path = obfuscated_file_path.replace(".gd", "_restored.gd")
    else: output_file_path = obfuscated_file_path
    

    identifiers = {}
    identifiersPresent = False
    comments = []
    commentsPresent = False
    restored_code = []

    with open(mapping_file_path, 'r') as file:
        obfuscated_source = json.load(file) # Load JSON file content
        # Retrieve vital data
        for scripts, data in obfuscated_source.items():
            if isDirectory: script = relative_path
            else:
                script = os.path.basename(obfuscated_file_path)
                if script.endswith("_obfuscated.gd"): script = script.replace("_obfuscated.gd", ".gd")
            if script in scripts:
                for data in obfuscated_source[script]:
                    obfuscated_content = obfuscated_source[script][data]
                    if data == "name_map":
                        # Retrieve original identifiers
                        for keyword in obfuscated_content.values():
                            for original_name in keyword.keys():
                                identifiers[original_name] = keyword[original_name]
                        if identifiers != {}: identifiersPresent = True
                    elif data == "comments":
                        # Retrieve comments
                        for comment, details in obfuscated_content.items():
                            comments.append([comment, details["line_number"], details["starting_index"]])
                        if comments != []: commentsPresent = True
    
    with open(obfuscated_file_path, 'r') as file:
        lines = file.readlines()    
        # Restore code
        for line_number, line in enumerate(lines):
            # Restore identifiers
            for original_name, obfuscated_name in identifiers.items():
                if isinstance(obfuscated_name, list): obfuscated_name = obfuscated_name[0]
                line = line.replace(obfuscated_name, original_name)
            # Restore comments
            for comment, line_num, start_pos in comments:
                # print(comment, line_num, start_pos)
                if line_number + 1 == line_num:
                    # print(line_number + 1, ".: " + line)
                    # print(line_num, ".: " + comment)
                    line = line[:start_pos] + f"{comment}" + line[start_pos:]
            restored_code.append(line)
    
    # Write the restored code back to the specified file
    with open(output_file_path, 'w') as file: file.writelines(restored_code)

    #Display the outcome
    if not identifiersPresent: print("No identifers found.")
    else: print("Identifiers restored.")
    if not commentsPresent: print("No comments found.")
    else: print("Comments restored.")
    if identifiersPresent or commentsPresent: print("Restoration complete.")

def main():
    input_path = input("Enter a file path or directory containing obfuscated GDScript files: ")
    # Cleanup input
    input_path = input_path.replace("'", "") # Remove single quotes
    input_path = input_path.replace('"', "") # Remove double quotes

    overwrite = input("Do you want to overwrite the file provided? (yes/no): ").strip().lower() == "yes"
    
    delete_obfuscated_code = input("Do you want to delete the obfuscated data after restoration? (yes/no): ").strip().lower() == "yes"

    # Check if the input is a directory or a file
    isDirectory = os.path.isdir(input_path)
    if os.path.isfile(input_path) and input_path.endswith(".gd"):
        obfuscated_file_path, filename_ob, mapping_file = check_for_obfuscation_suffixes(input_path)
        if os.path.exists(mapping_file): 
            print(f"Restoring original code from \"{os.path.basename(mapping_file)}\"...")
            restore_gdscript(obfuscated_file_path, mapping_file, overwrite, isDirectory, relative_path="./")

            # Delete files when done
            if delete_obfuscated_code:
                if not overwrite: os.remove(filename_ob)
                os.remove(mapping_file)
                print("Obfuscated code and obfuscation data file deleted")
        else:
            return print(f"Mapping file for \"{os.path.basename(obfuscated_file_path)}\" not found. Please ensure it is in the same directory as the file provided.")
            
    elif isDirectory:
        for suffix in ["_obfuscated", "_restored"]:
            if input_path.endswith(suffix):
                objective_root_path = remove_suffix(input_path, suffix)
                break
            else: objective_root_path = input_path
        objective_root_folder = os.path.basename(objective_root_path)

        # Derive mapping file
        if input_path.endswith("_obfuscated"): mapping_file = input_path[:-len("_obfuscated")] + "_obfuscation_data.json"
        else: mapping_file = input_path + "_obfuscation_data.json"
        
        # Determine overwrite status
        if not overwrite:
            # Create the new folder path for obfuscation
            if input_path.endswith("_obfuscated"): restored_folder_path =  input_path[:-len("_obfuscated")] + "_restored"
            else: restored_folder_path = input_path + "_restored"
            if os.path.exists(restored_folder_path):
                overwrite_res = input(f"There is already a folder called {os.path.basename(restored_folder_path)}. Do you want to overwrite it? (yes/no): ").strip().lower() == "yes"
                if overwrite_res:
                    shutil.rmtree(restored_folder_path)
                    shutil.copytree(input_path, restored_folder_path)
                    print(f"Restoring the source code in \"{os.path.basename(input_path)}\" as \"{os.path.basename(restored_folder_path)}\"...")
                else:
                    print("Terminating operation...")
                    time.sleep(1)
                    print("Operation terminated.")
                    return
            else: shutil.copytree(input_path, restored_folder_path)
            obfuscated_folder_path = input_path
            input_path = restored_folder_path
        
        if os.path.exists(mapping_file):
            # Walk through the directory
            for folder, subfolderNames, files in os.walk(input_path):
                for file in files:
                    # Check if the file has a .gd extension
                    if file.endswith(".gd"):
                        file_path = os.path.join(folder, file)
                        relative_path = os.path.relpath(file_path, mapping_file)[3:]
                        if not overwrite: 
                            objective_relative_path = os.path.join(objective_root_folder, os.path.join(*relative_path.split(os.sep)[1:]))
                            relative_path = objective_relative_path
                        print(f"Restoring the original code in \"{file}\"...")
                        restore_gdscript(file_path, mapping_file, overwrite, isDirectory, relative_path)
            #Delete files when done
            if delete_obfuscated_code:
                if not overwrite: os.remove(obfuscated_folder_path)
                os.remove(mapping_file)
                print("Obfuscated code and obfuscation data file deleted")
        else:
            return print(f"Mapping file \"{os.path.basename(mapping_file)}\" not found. Please ensure it is in the same directory as the folder provided.")
    else:
        return print("The specified path is not valid. Please enter a valid directory or a .gd file.")

if __name__ == '__main__':
    print("GDScript Code (Un)Obfuscator")
    print("----------------------------\n")
    main()
