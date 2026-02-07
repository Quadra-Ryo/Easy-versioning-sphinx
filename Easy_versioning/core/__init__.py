"""Core functionality for Easy Versioning."""

from .config import BuildConfiguration
from .workspace import WorkspaceManager
from .version_manager import VersionManager

__all__ = ['BuildConfiguration', 'WorkspaceManager', 'VersionManager']
