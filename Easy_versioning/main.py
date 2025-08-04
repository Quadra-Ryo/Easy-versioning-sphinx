import os
import shutil
import stat
import subprocess
import sys 
import threading
import http.server
import socketserver
import webbrowser
import time

default_language = "English"
clean_website = True

# Get the terminal path from which the script is executed
BASE_DIR = os.getcwd()
MODULE_DIR = os.path.dirname(os.path.abspath(__file__)) # Main script folder
DEFAULT_FOOTER = os.path.join(MODULE_DIR, "data", "footer.md")

# Initialize paths used throughout the script
FOOTER_PATH = os.path.join(BASE_DIR, "data")
SRC_PATH = os.path.join(BASE_DIR, "src")
BUILD_PATH = os.path.join(BASE_DIR, "project")
TEMP_PATH = os.path.join(BASE_DIR, "_temp")

################################################################################## Utils Functions

# Basic logging functions
def error(message):
    print(f"\033[1;31mERROR: {message}\033[0m")

def warning(message):
    print(f"\033[33mWARNING: {message}\033[0m")

def info(message):
    print(f"\033[34m{message}\033[0m")

def success(message):
    print(f"\033[32m{message}\033[0m")

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
        build_path = os.path.join(BUILD_PATH, "build")
        if os.path.exists(build_path):
            shutil.rmtree(build_path, onexc=handle_remove_readonly)
        
        # Cleaning the old "_temp" folder
        if os.path.exists(TEMP_PATH):
            shutil.rmtree(TEMP_PATH, onexc=handle_remove_readonly)
        
        info("Cleaned up the old folders.")
        
        # Creating "_temp" folder and its subfolders   
        dir_name = TEMP_PATH
        os.mkdir(dir_name)
        dir_name = os.path.join(TEMP_PATH, "src")
        os.mkdir(dir_name)
        dir_name = os.path.join(TEMP_PATH, "data")
        os.mkdir(dir_name)
        
        info("Created the \"_temp\" folder.")
        
        # Creating folder to build the final project
        dir_name = os.path.join(BUILD_PATH, "build")
        os.makedirs(dir_name, exist_ok=True)
        
        info("Created the final build folder.")
        
        # Copying the input data to the "_temp" folder to keep the src clean
        shutil.copytree(SRC_PATH, os.path.join(TEMP_PATH, "src"), dirs_exist_ok=True)
        footer_path = os.path.join(FOOTER_PATH, "footer.md")
        if os.path.exists(footer_path):
            shutil.copy(footer_path, os.path.join(TEMP_PATH, "data", "footer.md"))
        else:
            warning(f"Using the default footer: {DEFAULT_FOOTER}")
            shutil.copy(DEFAULT_FOOTER, os.path.join(TEMP_PATH, "data", "footer.md"))

        info("Data has been copied successfully.")
                 
    except PermissionError:
        error(f"Permission denied: Cannot create or delate '{dir_name}'.")
    except Exception as e:
        error(f"An unexpected error occurred during initial setup: {e}.")

# Final cleanup by deleting the "_temp" folder and all contained files.
def final_cleaning():
    """
    Remove temporary folders after the build process.
    """

    try:
        if os.path.exists(TEMP_PATH):
            shutil.rmtree(TEMP_PATH, onexc=handle_remove_readonly)
            info(f"Deleted temporary directory: '{TEMP_PATH}'.")
    except PermissionError:
        error(f"Permission denied: Cannot delete '{TEMP_PATH}'.")
    except Exception as e:
        error(f"An unexpected error occurred during cleanup: {e}.")
 
def check_default_language(versions):
    """
    Checking for the presence of the default language inside all the versions folders.
    """

    output = 0

    # Checking for the correct language but wrongly written or checking if in some versions I don't have the default language folder
    for version in versions:
        language_path = os.path.join(SRC_PATH,version,default_language)       
        if(not(os.path.exists(language_path))):
            output = -1
     
    return output

 ################################################################################## Data handling functions

 # Functions to retrieve versions from the src dir
def get_versions():

    """
    Retrieve all available documentation versions from the source directory.
    """

    versions = []
    version_list_str = ""

    for folder in os.listdir(f"{TEMP_PATH}/src"):
        if "_" not in folder:
            versions.append(folder)
            version_list_str += folder + ", "

    version_list_str = version_list_str.rstrip(", ")
    info(f"Found documentation versions: {version_list_str}.")
    return versions


# Adding all the project data to the standard footer
def project_data_setup(versions):
    """
    Update the footer template with available documentation versions.
    """
    
    # Formatting the versions as a JS Array
    version_list = "[" + ", ".join(f'"{v}"' for v in versions) + "]" # Example [English, Italiano, ...]

    # "\t" is used to indent the HTML code properly in the file
    html_versions = "\n".join(
        f"{'\t' if i == 0 else '\t\t\t\t'}<a href=\"#\" role=\"option\">{v}</a>"
        for i, v in enumerate(versions)
    )

    with open(f"{TEMP_PATH}/data/footer.md", "r") as footer_file:
        footer = footer_file.read()
    
    # Replacing the file placeholders
    footer = footer.replace("{html_v}", html_versions)
    footer = footer.replace("{v_list}", version_list)
    footer = footer.replace("{default_language}", default_language)

    with open(f"{TEMP_PATH}/data/footer.md", "w") as footer_file:
        footer_file.write(footer)

    # Printing the usefull infos  
    info(f"Updated footer with versions: {html_versions}.")    
    info(f"Updated footer with versions: {version_list}.")    
    info(f"Updated footer with versions: {default_language}.")

# Adding the actual versioning script to all the ".md" files
def add_versioning(versions):

    """
    Append versioning information to all Markdown files.
    """

    version_languages = []

    for version in versions:
        info(f"Processing version: {version}.")
        # Retrieve available languages for the current version and update the footer accordingly
        languages = languages_current_version_setup(version)
        version_languages.append((version, languages))

        for language in languages:
            info(f"Adding versioning for: {version} / {language}.")
            # Adding the current language to the footer file
            change_language(language)
            lang_path = f"{TEMP_PATH}/src/{version}/{language}"
            # Getting all the ".md" files inside the folders
            md_files = find_md(lang_path)

            with open(f"{TEMP_PATH}/data/temp_footer.md", "r") as footer_file:
                footer_content = footer_file.read()

            for md_file in md_files:
                with open(md_file, "a") as file:
                    file.write("\n\n\n" + footer_content)

            success(f"Added footer to all Markdown files in: {version} / {language}.")
            # Going back to the placeholder after finishing with the current language
            change_language(language)
            
    return version_languages

# Retriving all the available languages for a specific version of the documentation
def languages_current_version_setup(version):

    """
    Retrieve all available languages for a specific version.
    """

    info(f"Retriving the languages inside the version {version}.")

    html_languages = ""
    languages = []
    
    # Creating a copy of the "standard project" footer where I'm gonna add only the specific version/file data
    shutil.copy(f"{TEMP_PATH}/data/footer.md", f"{TEMP_PATH}/data/temp_footer.md")

    # Variables intitial set-up
    language_list = "["
    version_path = f"{TEMP_PATH}/src/{version}"

        
    with open(f"{TEMP_PATH}/data/temp_footer.md", "r") as footer_file:
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
    footer = footer.replace("{default_language}", default_language)

    with open(f"{TEMP_PATH}/data/temp_footer.md", "w") as footer_file:
        footer_file.write(footer)
        
    info(f"Found languages for version '{version}': {language_list}.")
    return languages

# Function used to switch from the language placeholder to the current language and back to the placeholder
def change_language(language):

    """
    Insert the selected language into the temporary footer file.
    """

    with open(f"{TEMP_PATH}/data/temp_footer.md", "r") as footer_file:
        footer = footer_file.read()

    # Replacing the placeholder with the languages the first time and than back with the placeholder
    if("{language}" in footer):
        footer = footer.replace("{language}", language)
    else:
        footer = footer.replace(f"{language}</s", "{language}</s")
        
    with open(f"{TEMP_PATH}/data/temp_footer.md", "w") as footer_file:
        footer_file.write(footer)

# Function that search for all the ".md" files inside of a directory
def find_md(directory):

    """
    Recursively find all Markdown files in a directory, excluding folders starting with '_'.
    """

    info(f"Retrieving all the \".md\" files inside the directory '{directory}'.")

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
    
    # Creating the sphinx build command string
    command = ["python", "-m", "sphinx", "-b", "html", ".", "_build/html"]

    for version, languages in version_languages:
        for language in languages:
            # Moving in the current folder
            BUILD_PATH = os.path.join(TEMP_PATH, "src", version, language)
            info(f"Building documentation for: {version} / {language}.")

            if os.path.exists(BUILD_PATH):
                try:
                    # Running the build command inside of the specific folder
                    result = subprocess.run(
                        command, capture_output=True, text=True, cwd=BUILD_PATH
                    )

                    if result.returncode == 0:
                        success(f"Build successful for: {version} / {language}.")
                    else:
                        error(f"Build failed for: {version} / {language}.")
                        error(f"{result.stderr}.")
                except Exception as e:
                    error(f"Exception during build for {version} / {language}: {e}.")
            else:
                error(f"Path not found: {BUILD_PATH}.")

# Set up the build folder with all required versions and files for the website to function correctly
def setup_build_folder(version_languages):

    """
    Copy built HTML files to the final project/build directory.
    """

    for version, languages in version_languages:
        # Setting up the version in the path
        version_BUILD_PATH = f"{BUILD_PATH}/build/{version}"
        os.makedirs(version_BUILD_PATH, exist_ok=True)
        info(f"Created directory: {version_BUILD_PATH}")

        for language in languages:
            # Setting up the language in the path for every language inside the current version folder
            language_BUILD_PATH = f"{version_BUILD_PATH}/{language}"
            os.makedirs(language_BUILD_PATH, exist_ok=True)
            info(f"Created directory: {language_BUILD_PATH}")

            source_html = f"{TEMP_PATH}/src/{version}/{language}/_build/html"
            
            if clean_website:
                shutil.rmtree(f"{source_html}/_sources", onexc=handle_remove_readonly)
                
            shutil.copytree(source_html, language_BUILD_PATH, dirs_exist_ok=True)
            success(f"Copied build files to: {language_BUILD_PATH}")

# Adding the bat file in the build path to give a quick start menu using cmd
def add_bat(version_languages):

    """
    Build and adds a simple bat file used to start a python tcp server.
    """

    latest_version = version_languages[len(version_languages)-1][0] # Getting the last available version from the data in input
    info(f"Latest version {latest_version}")

    bat_file =  (
                f'cd "{BUILD_PATH}/build"\n'
                'start /b python -m http.server 8000 --bind 0.0.0.0\n'
                'timeout /t 2 /nobreak\n'
                f'explorer "http://localhost:8000/{latest_version}/{default_language}/index.html"'
                )

    info(bat_file)
    # Creating the bat file
    with open(f"{BUILD_PATH}/build/start_server.bat", "w") as f:
        f.write(bat_file)

    return [latest_version, default_language]

# Starting a quick server on port 8000 to give the user immediate feedback on the documentation.
def start_quick_server(latest_version, default_language):

    """
    Start a static HTTP server on localhost:8001 and open the documentation homepage.
    """

    port = 8001 # Not 8000 to not use the same port as the bat file's server
    root_path = os.path.join(BUILD_PATH, "build")
    os.chdir(root_path)

    url = f"http://localhost:{port}/{latest_version}/{default_language}/index.html"
    
    # Server variables
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), handler)

    def serve():
        info(f"Serving documentation at: {url}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()
        info("Server shut down.")

    # Start the server in a different thread
    thread = threading.Thread(target=serve)
    thread.daemon = True
    thread.start()

    # Waiting for the server to open correctly
    time.sleep(1)

    # Giving quick access using the console to the user
    success(f"\n\nServer is running,  Visit your documentation at:\n{url.replace(" ", "%20")}")

    try:
        input("Press Enter to stop the server...\n")
    except KeyboardInterrupt:
        print("\nServer interrupted by user.")

# Main building function
def easy_versioning_build():

    """
    Calling all the functions .
    """
     
    global default_language
    global clean_website
    
    status = 0

    args = sys.argv[1:]  # Takes the parameters from the command line
    language = args[0] if len(args) > 0 else None
    clean = args[1] if len(args) > 1 else None

    # Checking for the inputted parameters
    if language is not None:
        info(f"Setting up the default language to {language}.")
        default_language = language

    if clean is not None and int(clean) == 0:
        info("Setting up the cleaning project process to false.")
        clean_website = False

    # Main process 
    info("Starting build configuration.")
    
    info("Initial checks")
    if not (os.path.exists(SRC_PATH)):
        error("No source folder found. Exiting.")
        exit(1)

    # Set up workspace folders used by the tool during execution
    info("Initial set-up:")
    initial_setup()
    success("Initial folder setup completed.")
    
    # Getting the versions of the documentation in the src folder
    info("Getting all the versions:")
    versions = get_versions()
    if not versions:
        error("No documentation versions found. Exiting.")
        exit(1)
    success("Retrieved all documentation versions.")
    
    status = check_default_language(versions)
    if status == -1:
        warning("The default language is not present in every version of the documentation! This may cause problems")

    # Initial set-up of the footer
    info("Setting up the versions data:")
    project_data_setup(versions)
    success("Setup ended.")

    # Adding the versioning script to the ".md" files
    info("Adding versioning to all the Markdown files:")
    version_languages = add_versioning(versions)
    success("Versioning added to all Markdown files.")

    # Building the project with the sphinx build command
    info("Starting to build the project:")
    build_project(version_languages)
    success("Project built successfully.")
    
    # Setting up the final project folder
    info("Organizing the folders to have a ready to use website")
    setup_build_folder(version_languages)
    success("All build files organized in 'project/build' directory.")

    # Setting up the BAT file to start a simple Python server for hosting the website
    info("Creating a simple .bat file to start a python server on port 8000 to test the website")
    info("Use this .bat file if you want to use advanced features like 3D files rendering")
    link_data = add_bat(version_languages) # Getting the latest version and default language
    success(".bat file created in the build folder")

    # Cleaning the project folders
    info("Final cleaning process:")
    final_cleaning()
    success("Build process completed successfully.")

    start_quick_server(link_data[0], link_data[1])

################################################################################## Main

if __name__ == "__main__":
    easy_versioning_build()