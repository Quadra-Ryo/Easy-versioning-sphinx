"""Version and language management for Easy Versioning."""

import os
from ..utils import info, warning

class VersionManager:
    """Manages documentation versions and their available languages."""
    
    def __init__(self, temp_src_path, src_path, default_language="English"):
        self.temp_src_path = temp_src_path
        self.src_path = src_path
        self.default_language = default_language
    
    def get_versions(self):
        """
        Retrieve all available documentation versions from the source directory.
        """
        versions = []
        version_list_str = ""

        for folder in os.listdir(self.temp_src_path):
            if "_" not in folder:
                versions.append(folder)
                version_list_str += folder + ", "

        version_list_str = version_list_str.rstrip(", ")
        info(f"Found documentation versions: {version_list_str}.")
        return versions
    
    def check_default_language(self, versions):
        """
        Checking for the presence of the default language inside all the versions folders.
        """
        output = 0

        # Checking for the correct language but wrongly written or checking if in some versions I don't have the default language folder
        for version in versions:
            language_path = os.path.join(self.src_path, version, self.default_language)       
            if not os.path.exists(language_path):
                output = -1
         
        return output
    
    def get_languages_for_version(self, version):
        """
        Retrieve all available languages for a specific version.
        """
        info(f"Retriving the languages inside the version {version}.")

        languages = []
        version_path = os.path.join(self.temp_src_path, version)

        for folder in os.listdir(version_path):
            if "_" not in folder:  # Exclude folders starting with "_"
                languages.append(folder)

        language_list = "[" + ", ".join(f'"{lang}"' for lang in languages) + "]"
        info(f"Found languages for version '{version}': {language_list}.")
        return languages
