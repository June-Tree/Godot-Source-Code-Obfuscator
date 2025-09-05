import os
import re


def remove_suffix(name, suffix):
    if name.endswith(suffix):
        return name[:-len(suffix)]
    return name

def check_for_obfuscated_suffix(file_path):
    #Create a variable that has (forcefully) has the obfuscated suffix
    suffixes = ['.gd', '_obfuscated.gd']
    # Check and remove the suffix to get the base name
    for suffix in suffixes:
        if file_path.endswith(suffix):
            # Remove the suffix and return the base name + obfuscated suffix
            filename_ob = file_path[:-len(suffix)] + '_obfuscated.gd'
            mapping_file = file_path[:-len(suffix)] + '_name_map.txt'
            break
    
    # folder = os.listdir(file_path)
    folder = file_path.rsplit('/', 1)[0]
    if file_path.endswith('_obfuscated.gd'):
        return file_path, filename_ob, mapping_file
    else: #Look for a duplicate with the obfuscated suffix
      for file in folder:
        if file.endswith('_obfuscated.gd') and remove_suffix(file, '_obfuscated.gd') == remove_suffix(file_path, '.gd'): #Compare files
          obfuscated_file = os.path.join(folder, file)
          return obfuscated_file, filename_ob, mapping_file
      #Then either the original file was overwritten, or no obfuscated version exists
      return file_path, filename_ob, mapping_file

def restore_gdscript(obfuscated_file_path, mapping_file_path, overwrite):
    with open(obfuscated_file_path, 'r') as file: obfuscated_source = file.read()

    # Read the name mapping from the mapping file
    name_map = {}
    with open(mapping_file_path, 'r') as file:
        for line in file:
            original, obfuscated = line.strip().split(' -> ')
            name_map[obfuscated] = original

    # Restore original names in the obfuscated source code
    for obfuscated, original in name_map.items():
        obfuscated_source = re.sub(r'\b' + re.escape(obfuscated) + r'\b', original, obfuscated_source)

    # Determine output file path
    if overwrite: output_file_path = obfuscated_file_path.replace('_obfuscated.gd', '.gd')
    else: output_file_path = obfuscated_file_path.replace('.gd', '_restored.gd')

    # Write the restored code back to the specified file
    with open(output_file_path, 'w') as file: file.write(obfuscated_source)

def main():
    obfuscated_file_path = input("Enter the directory or file path of the obfuscated GDScript files: ")

    overwrite_input = input("Do you want to overwrite the original file? (yes/no): ").strip().lower()
    overwrite = overwrite_input == 'yes'

    # Check if the input is a directory or a file
    if os.path.isfile(obfuscated_file_path) and obfuscated_file_path.endswith('.gd'):
        obfuscated_file_path, filename_ob, mapping_file = check_for_obfuscated_suffix(obfuscated_file_path)
        if os.path.exists(mapping_file): 
          print(f"Restoring original code from {os.path.basename(obfuscated_file_path)}...")
          restore_gdscript(obfuscated_file_path, mapping_file, overwrite)
          if os.path.exists(filename_ob): os.remove(filename_ob)
          os.remove(mapping_file)
          print("Restoration complete.")
        else:
          print(f"Mapping file for {obfuscated_file_path} not found. Please ensure it exists.")
          return
    elif os.path.isdir(obfuscated_file_path):
        # Walk through the directory
        for folder, subfolderNames, files in os.walk(obfuscated_file_path):
            for filename in files:
                # Check if the file has a .gd extension
                if filename.endswith('.gd'):
                    file_path=os.path.join(folder, filename)
                    file, file_ob, mapping_file = check_for_obfuscated_suffix(file_path)
                    if os.path.exists(mapping_file):
                      print(f"Restoring original code of \"{filename}\" with the mapping file {os.path.basename(mapping_file)}...")
                      restore_gdscript(file, mapping_file, overwrite)
                      if os.path.exists(file_ob): os.remove(file_ob)
                      os.remove(mapping_file)
                      print("Restoration complete.")
                    else:
                      print(f"Mapping file for \"{filename}\" not found. Please ensure it exists.")
                      continue
    else:
        print("The specified path is not valid. Please enter a valid directory or a .gd file.")

if __name__ == "__main__":
    print("GDScript Code (Un)Obfuscator")
    print("------------------------\n")
    main()
