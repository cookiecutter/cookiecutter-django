import os

def test_production_check():
    # Construct the absolute path to the manage.py file
    manage_py_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_project", "manage.py")
    
    # Assert that the manage.py file exists at the expected path
    assert os.path.exists(manage_py_path), f"Expected path {manage_py_path} does not exist."
