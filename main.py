from termcolor import colored

# Basic logging functions
def error(message):
    print(colored("Error: " + message, 'red'))


def warning(message):
    print(colored("Warning: " + message, 'yellow'))


def info(message):
    print(colored("Info: " + message, 'blue'))


def success(message):
    print(colored("Success: " + message, 'green'))
    
if __name__ == "__main__":
    # Main process
    info("Starting build configuration.")