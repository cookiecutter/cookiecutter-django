import os
import subprocess


def test_production_check():
    base_dir = os.getcwd()
    manage_py_path = os.path.join(base_dir, "test_project", "manage.py")
    subprocess.check_call(['python', manage_py_path, 'check', '--deploy'])