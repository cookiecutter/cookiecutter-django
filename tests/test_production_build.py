import subprocess

def test_production_check():
    # This will raise an exception if there's an error
    subprocess.check_call(['python', 'manage.py', 'check', '--deploy'])