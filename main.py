import os
import shutil
import stat
import subprocess

from termcolor import colored

DEFAULT_LANGUAGE = "English"
FOOTER_PATH = "data"
SRC_PATH = "src"
BUILD_PATH = "project"

################################################################################## Utils Functions

# Basic logging functions
def error(message):
    print(colored("Error: " + message, 'red'))


def warning(message):
    print(colored("Warning: " + message, 'yellow'))


def info(message):
    print(colored("Info: " + message, 'blue'))


def success(message):
    print(colored("Success: " + message, 'green'))

# Clearing the read-only to remove files without any problem
def handle_remove_readonly(func, path, exc_info):
    """
    Clear read-only attribute from a file and retry removal.
    """
    os.chmod(path, stat.S_IWRITE)
    func(path)    

################################################################################## Folders handling functions

# Initial set-up of the folders
def initial_setup():
    """
    Prepare the workspace by cleaning old builds and copying source files.
    """

    try:
        # Cleaning the old build if exists
        if os.path.exists(f"{BUILD_PATH}/build"):
            shutil.rmtree(f"{BUILD_PATH}/build", onexc=handle_remove_readonly)
        
        # Cleaning the old "_temp" folder
        if os.path.exists(f"_temp"):
            shutil.rmtree(f"_temp", onexc=handle_remove_readonly)
        
        info("Cleaned up the old folders.")
        
        # Creating "_temp" folder and its subfolders   
        dir_name = "_temp"
        os.mkdir(dir_name)
        dir_name = os.path.join("_temp", "src")
        os.mkdir(dir_name)
        dir_name = os.path.join("_temp", "data")
        os.mkdir(dir_name)
        
        info("Created the \"_temp\" folder.")
        
        # Creating folder to build the final project
        dir_name = os.path.join(BUILD_PATH, "build")
        os.makedirs(dir_name, exist_ok=True)
        
        info("Created the final build folder.")
        
        # Copying the input data to the "_temp" folder to keep the src clean
        shutil.copytree(SRC_PATH, os.path.join("_temp", "src"), dirs_exist_ok=True)
        shutil.copy(f"{FOOTER_PATH}/footer.md", os.path.join("_temp", "data", "footer.md"))
        
        info("Data has been copied successfully.")
                 
    except PermissionError:
        error(f"Permission denied: Cannot create or delate '{dir_name}'.")
    except Exception as e:
        error(f"An unexpected error occurred during initial setup: {e}")

# Final cleanup by deleting the "_temp" folder and all contained files.
def final_cleaning():
    """
    Remove temporary folders after the build process.
    """

    try:
        if os.path.exists("_temp"):
            shutil.rmtree("_temp", onexc=handle_remove_readonly)
            info(f"Deleted temporary directory: '{"_temp"}'.")
    except PermissionError:
        error(f"Permission denied: Cannot delete '{"_temp"}'.")
    except Exception as e:
        error(f"An unexpected error occurred during cleanup: {e}")
 
 ################################################################################## Data handling functions

 # Functions to retrieve versions from the src dir
def get_versions():
    """
    Retrieve all available documentation versions from the source directory.
    """

    versions = []
    version_list_str = ""

    for folder in os.listdir("_temp/src"):
        if "_" not in folder:
            versions.append(folder)
            version_list_str += folder + ", "

    version_list_str = version_list_str.rstrip(", ")
    info(f"Found documentation versions: {version_list_str}")
    return versions


# Adding all the project data to the standard footer
def project_data_setup(versions):
    """
    Update the footer template with available documentation versions.
    """
    
    # Formatting the versions as a JS Array
    version_list = "[" + ", ".join(f'"{v}"' for v in versions) + "]"

    # "\t" is used to indent the HTML code properly
    html_versions = "\n".join(
        f"{'\t' if i == 0 else '\t\t\t\t'}<a href=\"#\" role=\"option\">{v}</a>"
        for i, v in enumerate(versions)
    )

    with open("_temp/data/footer.md", "r") as footer_file:
        footer = footer_file.read()
    
    # Replacing the file placeholders
    footer = footer.replace("{html_v}", html_versions)
    footer = footer.replace("{v_list}", version_list)
    footer = footer.replace("{default_language}", DEFAULT_LANGUAGE)

    with open("_temp/data/footer.md", "w") as footer_file:
        footer_file.write(footer)

    # Printing the usefull infos  
    info(f"Updated footer with versions: {html_versions}")    
    info(f"Updated footer with versions: {version_list}")    
    info(f"Updated footer with versions: {DEFAULT_LANGUAGE}")

# Adding the actual versioning script to all the ".md" files
def add_versioning(versions):
    """
    Append versioning information to all Markdown files.
    """

    version_languages = []

    for version in versions:
        info(f"Processing version: {version}")
        # Retrieve available languages for the current version and update the footer accordingly
        languages = languages_current_version_setup(version)
        version_languages.append((version, languages))

        for language in languages:
            info(f"Adding versioning for: {version} / {language}")
            # Adding the current language to the footer file
            change_language(language)
            lang_path = f"_temp/src/{version}/{language}"
            # Getting all the ".md" files inside the folders
            md_files = find_md(lang_path)

            with open("_temp/data/temp_footer.md", "r") as footer_file:
                footer_content = footer_file.read()

            for md_file in md_files:
                with open(md_file, "a") as file:
                    file.write("\n\n\n" + footer_content)

            success(f"Added footer to all Markdown files in: {version} / {language}")
            # Going back to the placeholder after finishing with the current language
            change_language(language)
            
    return version_languages

# Retriving all the available languages for a specific version of the documentation
def languages_current_version_setup(version):
    """
    Retrieve all available languages for a specific version.
    """

    info(f"Retriving the languages inside the version {version}")

    html_languages = ""
    languages = []
    
    # Creating a copy of the "standard project" footer where I'm gonna add only the specific version/file data
    shutil.copy("_temp/data/footer.md", "_temp/data/temp_footer.md")

    language_list = "["
    version_path = f"_temp/src/{version}"

        
    with open("_temp/data/temp_footer.md", "r") as footer_file:
        footer = footer_file.read()

    for folder in os.listdir(version_path):
        if "_" not in folder:  # Exclude folders starting with "_"
            languages.append(folder)
            language_list += f'"{folder}", '

    # HTML code for the languages, \t used to proprely indent
    html_languages = "\n".join(
        f"{'\t' if i == 0 else '\t\t\t\t'}<a href=\"#\" role=\"option\">{lang}</a>"
        for i, lang in enumerate(languages)
    )

    # Removing the last wrong chars and closing the array
    language_list = language_list.rstrip(", ") + "]"

    # Replacing all the data of the current version of the documentation
    footer = footer.replace("{version}", version)
    footer = footer.replace("{html_l}", html_languages)
    footer = footer.replace("{l_list}", language_list)
    footer = footer.replace("{default_language}", DEFAULT_LANGUAGE)

    with open("_temp/data/temp_footer.md", "w") as footer_file:
        footer_file.write(footer)
        
    info(f"Found languages for version '{version}': {language_list}")
    return languages

# Function used to switch from the language placeholder to the current language and back to the placeholder
def change_language(language):
    """
    Insert the selected language into the temporary footer file.
    """

    with open("_temp/data/temp_footer.md", "r") as footer_file:
        footer = footer_file.read()

    if("{language}" in footer):
        footer = footer.replace("{language}", language)
    else:
        footer = footer.replace(f"{language}</s", "{language}</s")
        
    with open("_temp/data/temp_footer.md", "w") as footer_file:
        footer_file.write(footer)

# Function that search for all the ".md" files inside of a directory
def find_md(directory):
    """
    Recursively find all Markdown files in a directory, excluding folders starting with '_'.
    """

    info(f"Retrieving all the \".md\" files inside the directory '{directory}'")

    # Looping inside every directory that is not a "_" folder and getting every ".md" file path
    md_files = []
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if not d.startswith("_")]
        for file in files:
            if file.endswith(".md"):
                md_files.append(os.path.join(root, file))
    return md_files

# Function that runs the Sphinx build command for every version/language folder.
def build_project(version_languages):
    """
    Build the project using Sphinx for each version and language.
    """
    
    # Building the sphinx build command string
    command = ["python", "-m", "sphinx", "-b", "html", ".", "_build/html"]

    for version, languages in version_languages:
        for language in languages:
            build_path = os.path.join("_temp", "src", version, language)
            info(f"Building documentation for: {version} / {language}")

            if os.path.exists(build_path):
                try:
                    # Running the build command inside of the specific folder
                    result = subprocess.run(
                        command, capture_output=True, text=True, cwd=build_path
                    )

                    if result.returncode == 0:
                        success(f"Build successful for: {version} / {language}")
                    else:
                        error(f"Build failed for: {version} / {language}")
                        error(result.stderr)
                except Exception as e:
                    error(f"Exception during build for {version} / {language}: {e}")
            else:
                error(f"Path not found: {build_path}")
                
################################################################################## Main

if __name__ == "__main__":
    # Main process
    info("Starting build configuration.")
    
    # Set up workspace folders used by the tool during execution
    info("Initial set-up.")
    initial_setup()
    success("Initial folder setup completed.")
    
    # Getting the versions of the documentation in the src folder
    info("Getting all the versions")
    versions = get_versions()
    if not versions:
        error("No documentation versions found. Exiting.")
        exit(1)
    success("Retrieved all documentation versions.")
    
    # Initial set-up of the footer
    info("Setting up the versions data")
    project_data_setup(versions)
    success("Setup ended")

    info("Adding versioning to all the Markdown files")
    version_languages = add_versioning(versions)
    success("Versioning added to all Markdown files.")

    info("Starting to build the project")
    build_project(version_languages)
    success("Project built successfully.")
    
    # Cleaning the project folders
    info("Final cleaning process")
    final_cleaning()
    success("Build process completed successfully.")