import os
import sys
import shutil
import stat

# Addding the python tool
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Easy_versioning.main import initial_setup, final_cleaning, check_default_language, get_versions

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

def test_check_default_language():
    # Creating the needed folders
    if os.path.exists("src"):
        os.mkdir("src/V 1.0")
        os.mkdir("src/V 2.0")
        os.mkdir("src/V 1.0/English")
        os.mkdir("src/V 2.0/English")

    res = check_default_language(["V 1.0", "V 2.0"])

    # Checking the result
    if res == -1:
        assert False, "Check default language: Bad resault"

    # Removing the default language to check for errors cases
    shutil.rmtree("src/V 1.0/English",  onexc=handle_remove_readonly)
    shutil.rmtree("src/V 2.0/English",  onexc=handle_remove_readonly)
    
    res = check_default_language(["V 1.0", "V 2.0"])

    if res == 0:
        assert False, "Check default language: Bad resault"

    assert True
    
def test_get_versions():
    info("Running get_versions test")

    # Simulazione della struttura _temp/src
    os.makedirs("_temp/src/V1.0", exist_ok=True)
    os.makedirs("_temp/src/V2.0", exist_ok=True)
    os.makedirs("_temp/src/_private", exist_ok=True)  # Should be ignored

    versions = get_versions()

    expected_versions = ["V1.0", "V2.0"]
    if sorted(versions) != sorted(expected_versions):
        assert False, f"get_versions: Expected {expected_versions}, but got {versions}"

    success("get_versions working as expected")
    assert True

# Using the tests function before an official new version of the tool
if __name__ == "__main__":

    clean_folders()

    # Basic folder handling functions 
    test_initial_setup()
    test_final_cleaning()

    # Test finished
    success("Tests passed.")
    test_check_default_language()

    # Cleaning after testing the folder's handling functions
    clean_folders()

    # Project data handling functions tests
    test_get_versions()