import os
import shutil
import stat

from termcolor import colored

DEFAULT_LANGUAGE = "English"
FOOTER_PATH = "data"
SRC_PATH = "src"
BUILD_PATH = "project"

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
                 
    except FileExistsError:
        warning(f"Directory '{dir_name}' already exists.")
    except PermissionError:
        error(f"Permission denied: Cannot create '{dir_name}'.")
    except Exception as e:
        error(f"An unexpected error occurred during initial setup: {e}")
        

if __name__ == "__main__":
    # Main process
    info("Starting build configuration.")
    
    info("Initial set-up.")
    initial_setup()
    success("Initial folder setup completed.")
    
    