"""File operation utilities for Easy Versioning."""

import os
import stat

def handle_remove_readonly(func, path, exc_info):
    """
    Clear read-only attribute from a file and retry removal.
    """
    os.chmod(path, stat.S_IWRITE)
    func(path)
