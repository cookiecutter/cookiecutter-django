# Prevent push to remote main branch
import os
import sys

if __name__ == "__main__":
    # SKip check in CI
    if os.getenv("CI"):
        sys.exit(0)

    if os.getenv("PRE_COMMIT_REMOTE_BRANCH") == "refs/heads/main":
        print("pre-push hook: Can not push to remote main branch.")
        sys.exit(1)
