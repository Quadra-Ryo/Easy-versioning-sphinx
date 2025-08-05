import os
import sys
import shutil
import stat

# Addding the python tool
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Easy_versioning.main import initial_setup, final_cleaning

# Utils functions
def success(message):
    print(f"\033[32m{message}\033[0m")

def info(message):
    print(f"\033[34m{message}\033[0m")

def handle_remove_readonly(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    func(path)    

def clean_folders():
    if os.path.exists("src"):
        shutil.rmtree("src",  onexc=handle_remove_readonly)

    if os.path.exists("project"):
        shutil.rmtree("project",  onexc=handle_remove_readonly)

# Test functions
def test_initial_setup():
    info("Running initial set-up test")

    # Setting up the src folder to use the functions correctly
    if not(os.path.exists("src")):
        os.mkdir("src")

    # Function call
    initial_setup()

    # Checking if the folders were created
    if not(os.path.exists("project/build")) or not(os.path.exists("_temp")):
        assert False, "Initial_setup function: Impossible to create the initial folders"

    success("Initial set-up working")
    assert True

def test_final_cleaning():
    info("Running final cleaning test")

    # Function call
    final_cleaning()

    # Checking if the "_temp" folder was deleated
    if os.path.exists("_temp"):
        assert False, "Final cleaning function: Impossible to clean the folders"

    success("Final cleaning working")
    assert True

# Using the tests function before an official new version of the tool
if __name__ == "__main__":

    # Basic folder handling functions 
    test_initial_setup()
    test_final_cleaning()

    # Test finished
    success("Tests passed.")
    clean_folders()
