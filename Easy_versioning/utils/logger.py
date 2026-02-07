"""Logging utilities for Easy Versioning."""

def error(message):
    print(f"\033[1;31mERROR: {message}\033[0m")

def warning(message):
    print(f"\033[33mWARNING: {message}\033[0m")

def info(message):
    print(f"\033[34m{message}\033[0m")

def success(message):
    print(f"\033[32m{message}\033[0m")
