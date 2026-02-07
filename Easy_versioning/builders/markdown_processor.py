"""Markdown and RST file processor for Easy Versioning."""

import os
from ..utils import info, success

class MarkdownProcessor:
    """Processes markdown and RST files to add versioning footers."""
    
    def __init__(self, temp_path, temp_data_path, footer_builder):
        self.temp_path = temp_path
        self.temp_data_path = temp_data_path
        self.footer_builder = footer_builder
    
    def find_md(self, directory):
        """
        Recursively find all Markdown files in a directory, excluding folders starting with '_'.
        """
        info(f"Retrieving all the \".md\" files inside the directory '{directory}'.")

        # Looping inside every directory that is not a "_" folder and getting every ".md" file path
        source_files = []
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if not d.startswith("_")]
            for file in files:
                if file.endswith(".md") or file.endswith(".rst"):
                    source_files.append(os.path.join(root, file))
        return source_files
    
    def add_versioning(self, versions, temp_src_path):
        """
        Append versioning information to all Markdown files.
        """
        version_languages = []

        for version in versions:
            info(f"Processing version: {version}.")
            # Retrieve available languages for the current version and update the footer accordingly
            languages = self.footer_builder.languages_current_version_setup(version, temp_src_path)
            version_languages.append((version, languages))

            for language in languages:
                info(f"Adding versioning for: {version} / {language}.")
                # Adding the current language to the footer file
                self.footer_builder.change_language(language)
                lang_path = f"{temp_src_path}/{version}/{language}"
                # Getting all the ".md" files inside the folders
                source_files = self.find_md(lang_path)

                with open(f"{self.temp_data_path}/temp_footer.html", "r") as footer_file:
                    footer_content = footer_file.read()
                
                footer_content_rst = '.. raw:: html\n\n' + '\n'.join(f'\t{line}' for line in footer_content.splitlines())

                for source_file in source_files:
                    if source_file.endswith(".md"):    
                        with open(source_file, "a") as file:
                            file.write("\n\n\n" + footer_content)
                    else:
                        with open(source_file, "a") as file:
                            file.write("\n\n\n" + footer_content_rst)

                success(f"Added footer to all Markdown files in: {version} / {language}.")
                # Going back to the placeholder after finishing with the current language
                self.footer_builder.change_language(language)
                
        return version_languages
