"""Workspace management for Easy Versioning."""

import os
import shutil
from ..utils import info, warning, error, handle_remove_readonly

class WorkspaceManager:
    """Manages temporary workspace setup and cleanup."""
    
    def __init__(self, config):
        self.config = config
    
    def setup_workspace(self):
        """
        Prepare the workspace by cleaning old builds and copying source files.
        """
        try:
            # Cleaning the old build if exists
            build_path = os.path.join(self.config.build_path, "build")
            if os.path.exists(build_path):
                shutil.rmtree(build_path, onexc=handle_remove_readonly)
            
            # Cleaning the old "_temp" folder
            if os.path.exists(self.config.temp_path):
                shutil.rmtree(self.config.temp_path, onexc=handle_remove_readonly)
            
            info("Cleaned up the old folders.")
            
            # Creating "_temp" folder and its subfolders   
            dir_name = self.config.temp_path
            os.mkdir(dir_name)
            dir_name = os.path.join(self.config.temp_path, "src")
            os.mkdir(dir_name)
            dir_name = os.path.join(self.config.temp_path, "data")
            os.mkdir(dir_name)
            
            info("Created the \"_temp\" folder.")
            
            # Creating folder to build the final project
            dir_name = os.path.join(self.config.build_path, "build")
            os.makedirs(dir_name, exist_ok=True)
            
            info("Created the final build folder.")
            
            # Copying the input data to the "_temp" folder to keep the src clean
            shutil.copytree(self.config.src_path, os.path.join(self.config.temp_path, "src"), dirs_exist_ok=True)
            footer_path = os.path.join(self.config.footer_path, "footer.html")
            if os.path.exists(footer_path):
                shutil.copy(footer_path, os.path.join(self.config.temp_path, "data", "footer.html"))
            else:
                warning(f"Using the default footer: {self.config.default_footer}")
                shutil.copy(self.config.default_footer, os.path.join(self.config.temp_path, "data", "footer.html"))

            info("Data has been copied successfully.")
                     
        except PermissionError:
            error(f"Permission denied: Cannot create or delate '{dir_name}'.")
        except Exception as e:
            error(f"An unexpected error occurred during initial setup: {e}.")
    
    def cleanup_workspace(self):
        """
        Remove temporary folders after the build process.
        """
        try:
            if os.path.exists(self.config.temp_path):
                shutil.rmtree(self.config.temp_path, onexc=handle_remove_readonly)
                info(f"Deleted temporary directory: '{self.config.temp_path}'.")
        except PermissionError:
            error(f"Permission denied: Cannot delete '{self.config.temp_path}'.")
        except Exception as e:
            error(f"An unexpected error occurred during cleanup: {e}.")
