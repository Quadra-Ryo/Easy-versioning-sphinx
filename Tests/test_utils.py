import os
import sys

# Addding the python tool
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Easy_versioning.main import initial_setup, final_cleaning

def test_initial_setup():
    
    # Setting up the src folder to use the functions correctly
    if not(os.path.exists("src")):
        os.mkdir("src")

    # Function call
    initial_setup()

    # Checking if the folders were created
    if not(os.path.exists("project/build")) or not(os.path.exists("_temp")):
        assert False, "Initial_setup function: Impossible to create the initial folders"
    assert True

def test_final_cleaning():
    # Function call
    final_cleaning()

    # Checking if the "_temp" folder was deleated
    if os.path.exists("_temp"):
        assert False, "Final cleaning function: Impossible to clean the folders"

    assert True

# Using the tests function before an official new version of the tool
if __name__ == "__main__":

    # Basic folder handling functions 
    test_initial_setup()
    test_final_cleaning()

    # Test finished
    print("Tests passed.")
