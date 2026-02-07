"""Output organizer for Easy Versioning builds."""

import os
import shutil
from ..utils import info, success, handle_remove_readonly

class OutputOrganizer:
    """Organizes built documentation into the final output directory."""
    
    def __init__(self, temp_path, build_path, clean_website):
        self.temp_path = temp_path
        self.build_path = build_path
        self.clean_website = clean_website
    
    def setup_build_folder(self, version_languages):
        """
        Copy built HTML files to the final project/build directory.
        """
        for version, languages in version_languages:
            # Setting up the version in the path
            version_build_path = f"{self.build_path}/build/{version}"
            os.makedirs(version_build_path, exist_ok=True)
            info(f"Created directory: {version_build_path}")

            for language in languages:
                # Setting up the language in the path for every language inside the current version folder
                language_build_path = f"{version_build_path}/{language}"
                os.makedirs(language_build_path, exist_ok=True)
                info(f"Created directory: {language_build_path}")

                source_html = f"{self.temp_path}/src/{version}/{language}/_build/html"
                
                if self.clean_website:
                    shutil.rmtree(f"{source_html}/_sources", onexc=handle_remove_readonly)
                    
                shutil.copytree(source_html, language_build_path, dirs_exist_ok=True)
                success(f"Copied build files to: {language_build_path}")
    
    def add_bat(self, version_languages, default_language):
        """
        Build and adds a simple bat file used to start a python tcp server.
        """
        latest_version = version_languages[len(version_languages)-1][0] # Getting the last available version from the data in input
        info(f"Latest version {latest_version}")

        bat_file = (
                    f'cd "{self.build_path}/build"\n'
                    'start /b python -m http.server 8000 --bind 0.0.0.0\n'
                    'timeout /t 2 /nobreak\n'
                    f'explorer "http://localhost:8000/{latest_version}/{default_language}/index.html"'
                    )

        info(bat_file)
        # Creating the bat file
        with open(f"{self.build_path}/build/start_server.bat", "w") as f:
            f.write(bat_file)

        return [latest_version, default_language]
