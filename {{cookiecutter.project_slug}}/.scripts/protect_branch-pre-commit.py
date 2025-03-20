# Prevent commit to local main branch
import os
import subprocess
import sys

if __name__ == "__main__":
    # Skip check in CI
    if os.getenv("CI"):
        sys.exit(0)

    result = subprocess.run(["git", "symbolic-ref", "HEAD"], stdout=subprocess.PIPE, check=False)
    branch = result.stdout.decode("utf-8").strip()

    if branch == "refs/heads/main":
        print("pre-commit hook: Can not commit to the local main branch.")
        sys.exit(1)
