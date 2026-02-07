"""Configuration management for Easy Versioning."""

import os

class BuildConfiguration:
    """Holds all configuration paths and settings for the build process."""
    
    def __init__(self, base_dir, module_dir, default_language="English", clean_website=True):
        self.base_dir = base_dir
        self.module_dir = module_dir
        self.default_language = default_language
        self.clean_website = clean_website
        
        # Paths
        self.default_footer = os.path.join(module_dir, "data", "footer.html")
        self.footer_path = os.path.join(base_dir, "data")
        self.src_path = os.path.join(base_dir, "src")
        self.build_path = os.path.join(base_dir, "project")
        self.temp_path = os.path.join(base_dir, "_temp")
    
    @classmethod
    def from_current_directory(cls, module_dir, default_language=None, clean_website=True):
        """Create configuration from current working directory."""
        base_dir = os.getcwd()
        lang = default_language if default_language else "English"
        return cls(base_dir, module_dir, lang, clean_website)
    
    def validate(self):
        """Validate that required paths exist."""
        errors = []
        
        if not os.path.exists(self.src_path):
            errors.append("Source folder not found. Please create 'src' directory.")
        
        return len(errors) == 0, errors
