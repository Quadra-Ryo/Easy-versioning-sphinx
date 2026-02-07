"""Footer builder for Easy Versioning documentation."""

import os
import shutil
from ..utils import info

class FooterBuilder:
    """Builds and customizes HTML footers for documentation pages."""
    
    def __init__(self, temp_data_path, default_language):
        self.temp_data_path = temp_data_path
        self.default_language = default_language
    
    def project_data_setup(self, versions):
        """
        Update the footer template with available documentation versions.
        """
        # Formatting the versions as a JS Array
        version_list = "[" + ", ".join(f'"{v}"' for v in versions) + "]" # Example [English, Italiano, ...]

        # "\t" is used to indent the HTML code properly in the file
        html_versions = "\n".join(
            f"{'\t' if i == 0 else '\t\t\t\t'}<a href=\"#\" role=\"option\">{v}</a>"
            for i, v in enumerate(versions)
        )

        with open(f"{self.temp_data_path}/footer.html", "r") as footer_file:
            footer = footer_file.read()
        
        # Replacing the file placeholders
        footer = footer.replace("{html_v}", html_versions)
        footer = footer.replace("{v_list}", version_list)
        footer = footer.replace("{default_language}", self.default_language)

        with open(f"{self.temp_data_path}/footer.html", "w") as footer_file:
            footer_file.write(footer)

        # Printing the usefull infos  
        info(f"Updated footer with versions: {html_versions}.")    
        info(f"Updated footer with versions: {version_list}.")    
        info(f"Updated footer with versions: {self.default_language}.")
    
    def languages_current_version_setup(self, version, temp_src_path):
        """
        Retrieve all available languages for a specific version.
        """
        info(f"Retriving the languages inside the version {version}.")

        html_languages = ""
        languages = []
        
        # Creating a copy of the "standard project" footer where I'm gonna add only the specific version/file data
        shutil.copy(f"{self.temp_data_path}/footer.html", f"{self.temp_data_path}/temp_footer.html")

        # Variables intitial set-up
        language_list = "["
        version_path = f"{temp_src_path}/{version}"

            
        with open(f"{self.temp_data_path}/temp_footer.html", "r") as footer_file:
            footer = footer_file.read()

        for folder in os.listdir(version_path):
            if "_" not in folder:  # Exclude folders starting with "_"
                languages.append(folder)
                language_list += f'"{folder}", '

        # HTML code for the languages, \t used to proprely indent
        html_languages = "\n".join(
            f"{'\t' if i == 0 else '\t\t\t\t'}<a href=\"#\" role=\"option\">{lang}</a>"
            for i, lang in enumerate(languages)
        )

        # Removing the last wrong chars and closing the array
        language_list = language_list.rstrip(", ") + "]"

        # Replacing all the data of the current version of the documentation
        footer = footer.replace("{version}", version)
        footer = footer.replace("{html_l}", html_languages)
        footer = footer.replace("{l_list}", language_list)
        footer = footer.replace("{default_language}", self.default_language)

        with open(f"{self.temp_data_path}/temp_footer.html", "w") as footer_file:
            footer_file.write(footer)
            
        info(f"Found languages for version '{version}': {language_list}.")
        return languages
    
    def change_language(self, language):
        """
        Insert the selected language into the temporary footer file.
        """
        with open(f"{self.temp_data_path}/temp_footer.html", "r") as footer_file:
            footer = footer_file.read()

        # Replacing the placeholder with the languages the first time and than back with the placeholder
        if "{language}" in footer:
            footer = footer.replace("{language}", language)
        else:
            footer = footer.replace(f"{language}</s", "{language}</s")
            
        with open(f"{self.temp_data_path}/temp_footer.html", "w") as footer_file:
            footer_file.write(footer)
