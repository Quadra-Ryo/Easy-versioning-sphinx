"""Sphinx builder for Easy Versioning documentation."""

import os
import subprocess
from ..utils import info, error, success

class SphinxBuilder:
    """Manages Sphinx documentation builds."""
    
    def __init__(self, temp_path):
        self.temp_path = temp_path
    
    def build_project(self, version_languages):
        """
        Build the project using Sphinx for each version and language.
        """
        # Creating the sphinx build command string
        command = ["python", "-m", "sphinx", "-b", "html", ".", "_build/html"]

        for version, languages in version_languages:
            for language in languages:
                # Moving in the current folder
                build_path = os.path.join(self.temp_path, "src", version, language)
                info(f"Building documentation for: {version} / {language}.")

                if os.path.exists(build_path):
                    try:
                        # Running the build command inside of the specific folder
                        result = subprocess.run(
                            command, capture_output=True, text=True, cwd=build_path
                        )

                        if result.returncode == 0:
                            success(f"Build successful for: {version} / {language}.")
                        else:
                            error(f"Build failed for: {version} / {language}.")
                            error(f"{result.stderr}.")
                    except Exception as e:
                        error(f"Exception during build for {version} / {language}: {e}.")
                else:
                    error(f"Path not found: {build_path}.")
