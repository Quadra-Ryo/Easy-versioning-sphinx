"""
Unit tests for BuildConfiguration class.

This module contains tests for the configuration management functionality.
"""

import os
import pytest
from pathlib import Path

from easy_versioning.core.config import BuildConfiguration


class TestBuildConfiguration:
    """Test suite for BuildConfiguration class."""
    
    def test_initialization(self):
        """Test basic initialization of BuildConfiguration."""
        config = BuildConfiguration(
            base_dir="/home/user/docs",
            module_dir="/usr/lib/easy_versioning"
        )
        
        assert config.base_dir == "/home/user/docs"
        assert config.module_dir == "/usr/lib/easy_versioning"
        assert config.default_language == "English"
        assert config.clean_website is True
    
    def test_custom_initialization(self):
        """Test initialization with custom parameters."""
        config = BuildConfiguration(
            base_dir="/home/user/docs",
            module_dir="/usr/lib/easy_versioning",
            default_language="Italian",
            clean_website=False
        )
        
        assert config.default_language == "Italian"
        assert config.clean_website is False
    
    def test_property_paths(self):
        """Test that property paths are correctly constructed."""
        config = BuildConfiguration(
            base_dir="/home/user/docs",
            module_dir="/usr/lib/easy_versioning"
        )
        
        assert config.default_footer_path == "/usr/lib/easy_versioning/data/footer.html"
        assert config.footer_path == "/home/user/docs/data"
        assert config.src_path == "/home/user/docs/src"
        assert config.build_path == "/home/user/docs/project"
        assert config.temp_path == "/home/user/docs/_temp"
    
    def test_from_current_directory(self):
        """Test factory method for creating config from current directory."""
        config = BuildConfiguration.from_current_directory(
            module_dir="/usr/lib/easy_versioning"
        )
        
        assert config.base_dir == os.getcwd()
        assert config.module_dir == "/usr/lib/easy_versioning"
    
    def test_from_current_directory_with_overrides(self):
        """Test factory method with parameter overrides."""
        config = BuildConfiguration.from_current_directory(
            module_dir="/usr/lib/easy_versioning",
            default_language="German",
            clean_website=False
        )
        
        assert config.default_language == "German"
        assert config.clean_website is False
    
    def test_validate_missing_files(self):
        """Test validation with missing required files."""
        config = BuildConfiguration(
            base_dir="/nonexistent/path",
            module_dir="/nonexistent/module"
        )
        
        is_valid, errors = config.validate()
        
        assert not is_valid
        assert len(errors) > 0
        assert any("footer" in err.lower() for err in errors)
        assert any("source" in err.lower() for err in errors)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
