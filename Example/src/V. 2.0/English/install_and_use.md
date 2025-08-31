# How to Install and Use the Tool

## Installation

The tool is available on [PyPI](https://pypi.org/project/Easy-versioning/) and can be easily installed using the following command:

`pip install easy-versioning`

During installation, all packages listed in `requirements.txt` will also be installed, as they are essential for the tool’s functionality.

## Usage

First, structure your documentation project folders as follows:

📦 Easy_versioning_Sphinx/  
├── 📂 data/  
│   └── 📄 Footer.hmtl   
├── 📂 src/  
│   ├── 📁 V. X.XX/  
│   │   ├── 🌐 Language 1/  
│   │   │   └── 📘 Language 1 Sphinx Project/  
│   │   └── 🌐 Language 2/  
│   │       └── 📘 Language 2 Sphinx Project/  
│   ├── 📁 V. Y.YY/  
│   ├── 📁 V. Z.ZZ/


If a project has not yet been started, the `easy-versioning-setup` command can be used to automatically generate the structure shown above, thus simplifying the initial development phases.    
The `easy-versioning-setup` command accepts up to two optional parameters: the **project name** and the **author name**. If not specified, the default values "Documentation" and "Author" will be assigned.     
The input parameters will be used exclusively for creating the Sphinx project within the configured folders and must not contain spaces.     
Example:     
`easy-versioning-setup Test_Easy_Versioning Niccolò_Quadrani`   

Then open a terminal, navigate to the project’s root folder (in this example, `Easy_versioning_Sphinx/`), and run the command:
`Easy_versioning_build`

The `Easy_versioning_build` command accepts up to two optional parameters:

1. **Main language** (string): This is used for safe redirection when a specific version is missing in some languages. The language provided here must exist in all documentation versions to avoid issues.

2. **Source file retention** (integer): If set to `0`, source `.md` files will **not** be deleted from the final output. Any other value will result in their automatic removal to keep the project lighter and easier to deploy.

If no parameters are provided, the tool defaults to English as the main language and removes source files from the final build.

Files in the `src/` directory will **never be modified or deleted**. These parameters only affect the final build output.

## Version/Language Switcher Form

If you include a `data/` directory (alongside `src/`) containing a `footer.md` file, you can customize the documentation footer and integrate a form for switching between versions and languages.

A fully functional `footer.md` template is available at: [GitHub](https://github.com/Quadra-Ryo/Easy-versioning-sphinx/blob/main/Easy_versioning/footer.md).  
If `data/footer.md` is not provided, the default template from the link above will be applied.

Examples:  
- `easy_versioning_build` — Uses English as the default language and removes the `_source` directory.  
- `easy_versioning_build Italiano 0` — Sets "Italiano" as the default language (So the tool will search for the folder "Italiano" inside the versions folder) and keeps the `_source` directory intact.  
- `easy_versioning_build Deutsch` — Sets "Deutsch" as the default language and removes the `_source` directory.  
