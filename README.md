# <p align="center">Godot Source Code Obfuscator</p>

This repository contains a set of Python scripts designed for obfuscating and unobfuscating Godot source code files. The obfuscation process scrambles the names of declared constants, variables, functions, classes, and extends, while also removing comments to render the code unreadable. A name map is generated to facilitate unobfuscation.  
**This should be done on source files prior to exporting the game through the engine.**  
It works on Godot 4.0 and above

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Obfuscating Code](#obfuscating-code)
    - [Obfuscating a File](#prompts)
    - [Obfuscating a Folder](#obfuscating-a-folder)
    - [Example](#obfuscation-example)
  - [Unobfuscating Code](#unobfuscating-code)
    - [Unobfuscating a File](#unobfuscating-code)
    - [Unobfuscating a Folder](#unobfuscating-a-folder)
    - [Example](#unobfuscation-example)
- [Other ways to secure your code](#other-ways-to-secure-your-code)
- [Contributing](#contributing)
- [License](#license)
- [Authors notes](#authors-notes)

## Features

- **Obfuscation**: Convert readable Godot source code into a less understandable format by scrambling the names of identifiers
  - Ignoring `_ready` and `_process` functions
  - Including type aliases
- **Unobfuscation**: Restores the original code using the generated name map.
- **Comment Removal**: Removes comments to enhance code security.
- **Directory Handling**: Can process both individual files and entire folders.
- **Name Map Generation**: Creates a `.txt` file containing the name map for each `.gd` file.
- **Easy to Use**: Simply run the script you need directly or via a command-line interface and follow the prompts.

## Installation

To use the scripts, you need to have Python 3.x installed on your PC. You can download it from [python.org](https://www.python.org/downloads/).

Clone the repository:

```bash
git clone https://github.com/June-Tree/Godot-Source-Code-Obfuscator.git
cd godot-source-code-obfuscator/scripts
```

## Usage

### Obfuscating Code

To obfuscate a Godot source code file or folder, run the following command:

```bash
python <unobfuscation_script.py>
```

#### Prompts

1. **Directory path (file or folder)**: The script will handle it accordingly.

2. **Overwrite Original**: You will be asked if you want to overwrite the original file(s). **DO NOT SAY _"YES"_ IF THIS IS THE ONLY COPY YOU HAVE**. Saying "yes" will overwrite the file, while saying "no" will create a copy and obfuscate that instead.  
This prompt is essentally a guard rail to prevent data loss or irreversible damage.

3. **Name Length**: Enter the desired length for generated names. A number greater than 5 is recommended, and 10 or more is ideal when you have a lot of files.

#### Obfuscating a Folder

The script will walk through the provided folder and check every file in every subfolder for `.gd` files to obfuscate them.  
You will be asked if you would like to copy the folder structure for the name map files.

- Saying "yes" (recommended) will create a separate folder following the original structure, making unobfuscation easier.
- Saying "no" will create a separate folder with all name maps placed in the same location. Files with the same name will have an increment attached to prevent overwriting.  
This is fine if the number of `.gd` files is small, and you have no problem manually placing each file in their counterpart's locations, or if you just want everything in one place, and you feel you likely will need to fix bugs in individual files anyway. If not, it's best to say "yes".

#### Obfuscation example

```bash
python gdscript_obfuscator.py
```

___

### Unobfuscating Code

The unobfuscation process involves retrieving the scrambled data's initial form from the name map file(s) and restoring the code(s) to readable states.  
Make sure each obfuscated `.gd` file you would like to restore has its counterpart name map `.txt` in the same folder.  
Unfortunately, at this time, comments are not retrievable

#### Unobfuscating a Folder

- If when obfuscating, you chose to follow the original structure of the source code, all you'd need to do is copy and paste the contents of the name map folder into the obfuscated source code folder, and each name map file will be placed next to their respective files.
- If when obfuscating, you chose not to follow the original structure of the source code, you will need to manually copy and paste each individual `.gd` file to their counterpart's locations.  
**Don't forget to remove any increment attached at their ends, as this will cause them to be ignored, and the restoration for the related file to be skipped.**

To unobfuscate a previously obfuscated Godot source code file, use the following command:

```bash
python <unobfuscation_script.py>
```

#### Unobfuscation example

```bash
python gdscript_unobfuscator.py
```

## Other ways to secure your code

- Use type aliases
- Use compiled bytecode `.gdc` instead of plain text scripts
- Enable encription when exporting
- Encrypt Packed to secure the `.pck` file

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See [MIT License details](https://en.wikipedia.org/wiki/MIT_License).
Feel free to modify any sections or details to better fit your needs!

## Authors notes

### Future plans

- Remove empty lines left after removing comments
- Comment retrieval upon unobfuscation
- Obfuscate used-defined classes and their extends (across files)
- Scrambling scene names
- Scrambling asset names
- Randomizing file locations
  
Thanks for visiting!
