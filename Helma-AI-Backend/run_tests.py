#!/usr/bin/env python3
"""
Test runner script for the FastAPI Backend API.
"""
import pytest
import sys


def main():
    """
    Run tests with pytest and handle the exit code.
    
    Examples:
        python run_tests.py                 # Run all tests
        python run_tests.py -xvs            # Run all tests with more verbose output
        python run_tests.py tests/test_main.py  # Run tests from a specific file
    """
    # Use sys.argv to pass command line arguments to pytest
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    
    # Run pytest with specified arguments
    exit_code = pytest.main(args)
    
    # Exit with the same code as pytest
    sys.exit(exit_code)


if __name__ == "__main__":
    main() 