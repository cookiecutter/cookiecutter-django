import os
import subprocess
import pytest

def test_production_check():
    # Get the absolute path to the manage.py file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    manage_py_path = os.path.join(base_dir, '..', 'test_project', 'manage.py')

    # Ensure the path exists before proceeding
    assert os.path.exists(manage_py_path), f"Expected path {manage_py_path} does not exist."

    # Run the Django deployment checks
    subprocess.check_call(['python', manage_py_path, 'check', '--deploy'])