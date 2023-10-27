import os
import subprocess


def test_production_build():
    """Test production build."""
    # Run production build
    subprocess.run(["npm", "run", "build"], check=True)

    # Check that the build folder exists
    assert os.path.isdir("build")

    # Check that the build folder contains the index.html file
    assert os.path.isfile("build/index.html")

    # Check that the build folder contains the static folder
    assert os.path.isdir("build/static")


def test_production_build_with_env():
    """Test production build with environment variable."""
    # Set environment variable
    os.environ["REACT_APP_API_URL"] = "http://localhost:5000"

    # Run production build
    subprocess.run(["npm", "run", "build"], check=True)

    # Check that the build folder exists
    assert os.path.isdir("build")

    # Check that the build folder contains the index.html file
    assert os.path.isfile("build/index.html")

    # Check that the build folder contains the static folder
    assert os.path.isdir("build/static")

    # Unset environment variable
    del os.environ["REACT_APP_API_URL"]


def test_production_build_with_env_and_no_api_url():
    """Test production build with environment variable and no API URL."""
    # Set environment variable
    os.environ["REACT_APP_API_URL"] = ""

    # Run production build
    subprocess.run(["npm", "run", "build"], check=True)

    # Check that the build folder exists
    assert os.path.isdir("build")

    # Check that the build folder contains the index.html file
    assert os.path.isfile("build/index.html")

    # Check that the build folder contains the static folder
    assert os.path.isdir("build/static")

    # Unset environment variable
    del os.environ["REACT_APP_API_URL"]


def test_production_build_with_env_and_invalid_api_url():
    """Test production build with environment variable and invalid API URL."""
    # Set environment variable
    os.environ["REACT_APP_API_URL"] = "invalid"

    # Run production build
    subprocess.run(["npm", "run", "build"], check=True)

    # Check that the build folder exists
    assert os.path.isdir("build")

    # Check that the build folder contains the index.html file
    assert os.path.isfile("build/index.html")

    # Check that the build folder contains the static folder
    assert os.path.isdir("build/static")

    # Unset environment variable
    del os.environ["REACT_APP_API_URL"]


