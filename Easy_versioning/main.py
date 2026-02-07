"""Main entry point for Easy Versioning build commands."""

import os
import sys
import subprocess
import shutil

from .core import BuildConfiguration, WorkspaceManager, VersionManager
from .builders import FooterBuilder, MarkdownProcessor, SphinxBuilder, OutputOrganizer
from .utils import info, error, success, warning, handle_remove_readonly, ServerManager

def easy_versioning_build():
    """
    Calling all the functions.
    """
    # Get configuration from command line args
    args = sys.argv[1:]
    language = args[0] if len(args) > 0 else None
    clean = args[1] if len(args) > 1 else None

    # Get paths
    base_dir = os.getcwd()
    module_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create configuration
    default_language = language if language else "English"
    clean_website = True
    
    if language is not None:
        info(f"Setting up the default language to {language}.")

    if clean is not None and int(clean) == 0:
        info("Setting up the cleaning project process to false.")
        clean_website = False

    config = BuildConfiguration(base_dir, module_dir, default_language, clean_website)
    
    # Main process 
    info("Starting build configuration.")
    
    info("Initial checks")
    if not os.path.exists(config.src_path):
        error("No source folder found. Exiting.")
        exit(1)

    # Set up workspace folders used by the tool during execution
    info("Initial set-up:")
    workspace = WorkspaceManager(config)
    workspace.setup_workspace()
    success("Initial folder setup completed.")
    
    # Getting the versions of the documentation in the src folder
    info("Getting all the versions:")
    temp_src = os.path.join(config.temp_path, "src")
    version_mgr = VersionManager(temp_src, config.src_path, config.default_language)
    versions = version_mgr.get_versions()
    
    if not versions:
        error("No documentation versions found. Exiting.")
        exit(1)
    success("Retrieved all documentation versions.")
    
    status = version_mgr.check_default_language(versions)
    if status == -1:
        warning("The default language is not present in every version of the documentation! This may cause problems")

    # Initial set-up of the footer
    info("Setting up the versions data:")
    temp_data = os.path.join(config.temp_path, "data")
    footer_builder = FooterBuilder(temp_data, config.default_language)
    footer_builder.project_data_setup(versions)
    success("Setup ended.")

    # Adding the versioning script to the ".md" files
    info("Adding versioning to all the Markdown files:")
    md_processor = MarkdownProcessor(config.temp_path, temp_data, footer_builder)
    version_languages = md_processor.add_versioning(versions, temp_src)
    success("Versioning added to all Markdown files.")

    # Building the project with the sphinx build command
    info("Starting to build the project:")
    sphinx_builder = SphinxBuilder(config.temp_path)
    sphinx_builder.build_project(version_languages)
    success("Project built successfully.")
    
    # Setting up the final project folder
    info("Organizing the folders to have a ready to use website")
    output_organizer = OutputOrganizer(config.temp_path, config.build_path, config.clean_website)
    output_organizer.setup_build_folder(version_languages)
    success("All build files organized in 'project/build' directory.")

    # Setting up the BAT file to start a simple Python server for hosting the website
    info("Creating a simple .bat file to start a python server on port 8000 to test the website")
    info("Use this .bat file if you want to use advanced features like 3D files rendering")
    link_data = output_organizer.add_bat(version_languages, config.default_language)
    success(".bat file created in the build folder")

    # Cleaning the project folders
    info("Final cleaning process:")
    workspace.cleanup_workspace()
    success("Build process completed successfully.")

    # Start quick server
    server_mgr = ServerManager(config.build_path)
    server_mgr.start_quick_server(link_data[0], link_data[1])

def initial_set_up():
    """
    Simple easy-versioning project set-up.
    """
    try:
        info("Setting up the project structure")
        
        args = sys.argv[1:]
        title = args[0] if len(args) > 0 else "Documentation"
        author = args[1] if len(args) > 1 else "Author"

        base_dir = os.getcwd()
        module_dir = os.path.dirname(os.path.abspath(__file__))
        default_footer = os.path.join(module_dir, "data", "footer.html")

        src_path = os.path.join(base_dir, "src")

        version_paths = [
            [os.path.join(base_dir, "src", "V. 1.0", "English"), "1.0"],
            [os.path.join(base_dir, "src", "V. 2.0", "English"), "2.0"]
        ]

        info("Creating the versions and the sphinx projects")

        # Check if sphinx is available
        subprocess.run(["sphinx-quickstart", "--version"], capture_output=True, text=True, check=True)

        # Create version directories and initialize sphinx projects
        if not os.path.exists(src_path):
            for version in version_paths:
                version_dir = version[0]
                if os.path.exists(version_dir) and not os.path.isdir(version_dir):
                    error(f"Path exists but is not a directory: {version_dir}")
                    return
                
                os.makedirs(version[0], exist_ok=True)
                command = [
                    "sphinx-quickstart",
                    "--quiet",
                    "-p", title,
                    "-a", author,
                    "-v", version[1],
                    "--sep"
                ]
                
                try:
                    result = subprocess.run(command, capture_output=True, text=True, cwd=version[0])
                    if result.returncode == 0:
                        success(f"Sphinx set-up completed for {version[1]}.")
                    else:
                        error(f"Sphinx set-up failed for {version[1]}.")
                        error(f"{result.stderr}.")
                except Exception as e:
                    error(f"Exception during the set-up {e}.")
                    return

        # Handle data folder
        info("Handling the data function")
        data_path = os.path.join(base_dir, "data")

        if not os.access(base_dir, os.W_OK):
            error(f"Permission denied: Cannot write to {base_dir}")
            return
        
        if os.path.exists(data_path):
            try:
                shutil.rmtree(data_path, onexc=handle_remove_readonly)
            except Exception as e:
                error(f"Failed to remove directory {data_path}: {e}")
                return
        
        os.makedirs(data_path, exist_ok=True)

        if not os.path.exists(default_footer):
            error(f"Footer file does not exist: {default_footer}")
            return
        try:
            shutil.copy(default_footer, data_path)
            success(f"Copied footer from {default_footer} to {data_path}")
        except Exception as e:
            error(f"Failed to copy footer: {e}")
            return

        success("Initial set-up ended!")
    except Exception as e:
        error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    easy_versioning_build()
