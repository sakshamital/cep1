#!/usr/bin/env python3
"""CLI script to validate data integrity."""
import sys
import os

# Add parent directory to path so we can import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.repository import get_repo, RepositoryError


def main():
    try:
        get_repo().load()
        print("Data validation successful: No integrity errors or dependency cycles found.")
        sys.exit(0)
    except RepositoryError as e:
        print("Data validation failed:")
        print(e)
        sys.exit(1)


if __name__ == '__main__':
    main()
