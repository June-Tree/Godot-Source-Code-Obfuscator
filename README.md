# <p align="center">Godot Source Code Obfuscator</p>

This repository contains a set of Python scripts designed for obfuscating and unobfuscating Godot source code files.  The obfuscation process scrambles the names of declared identifiers, while also removing comments to render the code unreadable. A name map is generated to facilitate unobfuscation.  
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
    - [Example](#unobfuscation-example)
- [Extra info](#final-notes)
- [Other ways to help secure your code](#other-ways-to-help-secure-your-code)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Obfuscation**: Convert readable Godot source code into a less understandable format by scrambling the names of identifiers.
  - Including typed variable declarations (type aliases) and class definitions
  - Ignoring system functions
- **Comment Removal**: Removes comments to enhance code security.
- **Directory Handling**: Can process both individual files and entire folders.
- **Name Map Generation and Comments Backup**: Creates a `.json` file containing name and comment maps for each `.gd` file.  
<sub>The `.json` file is just the file or folder name paired with `_obfuscation_data` at the end, so `scriptFileOrFolderName_obfuscation_data.json`.  
If at any point you change the name of the original, you will need to change its name in the data file's name as well so the unobfuscation script can find it.</sub>
- **De-initializing (version control features and history removal)**: Removes any .git folder present in the root folder.
- **Unobfuscation**: Restores the original code using the generated obfuscation data.
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
<sub>Please provide an absolute path for accuracy</sub>

2. **Overwrite Original**: You will be asked if you want to overwrite the file/folder provided. **DO NOT SAY _"YES"_ IF THIS IS THE ONLY COPY YOU HAVE**. Saying "yes" will overwrite the file, while saying "no" will create a copy and obfuscate that instead.  
This prompt is essentially a guard rail to prevent data loss or irreversible damage.

3. **Name Length**: Enter the desired length for generated names. A number greater than 5 is recommended, and 10 or more is ideal when you have a lot of files, but if you really want to go crazy with it, numbers in the triple or quadruple digits would be fine as well.  
<sub>You can write a 100, and you will get a hundred characters. It's a minimum of 1, but there isn't really any maximum .^_^.</sub>

4. **Remove version control**: You will be asked if you want to remove version control. This is yet another guard rail to prevent irreversible damage. You are however advised to say "yes", as retaining it would still allow for the reversal of the obfuscation.  
<sub>You may still need to go in and get rid of any residual files that persist though.</sub>

#### Obfuscating a Folder

The script will walk through the provided folder and check every file in every subfolder for `.gd` files to obfuscate them. It will then create a `.json` file for the obfuscation data of the folder.

#### Obfuscation example

```bash
python gdscript_obfuscator.py
```

___

### Unobfuscating Code

The unobfuscation process involves retrieving the scrambled data's initial form from the obfuscation data file and restoring the code(s) to a readable state. Comments are also restored.  
**Please ensure that the relevant obfuscation data `.json` is in the same directory as the file/folder provided.**

To unobfuscate a previously obfuscated Godot source code file, use the following command:

```bash
python <unobfuscation_script.py>
```

#### Unobfuscation example

```bash
python gdscript_unobfuscator.py
```

## Final notes

Make sure to store the obfuscation data file in a safe location.  
<sub>The goal for this is to provide a lightweight means to obfuscate and retrieve obfuscated code, should you loose the original and only have access to obfuscated code. </sub>

If you're looking for a plugin for use from within godot itself, [GDMaim](https://github.com/cherriesandmochi/gdmaim) is an excellent tool for that.

### Future plans

- Scrambling scene names
- Scrambling asset names
- Randomizing file locations

## Other ways to help secure your code

- Use compiled bytecode `.gdc` instead of plain text scripts
- Enable encryption when exporting
- Encrypt Packed to secure the `.pck` file

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for more details.
Feel free to modify any sections or details to better fit your needs!

<br/>

<div align="center">Thanks for visiting! O<sub> _ </sub>O</div>
