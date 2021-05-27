import os
import sys

import uvicorn
from uvicorn.supervisors.watchgodreload import CustomWatcher


ignored = {
    "templates",
    "static",
    "staticfiles",
    "compose",
    ".ipython",
    "bin",
    ".pytest_cache",
    ".idea",
    "media",
    "htmlcov",
    "docs",
    "locale",
    "requirements",
}


class WatchgodWatcher(CustomWatcher):
    def __init__(self, *args, **kwargs):
        self.ignored_dirs.update(ignored)
        super(WatchgodWatcher, self).__init__(*args, **kwargs)


uvicorn.supervisors.watchgodreload.CustomWatcher = WatchgodWatcher
if __name__ == "__main__":
    sys.path.insert(0, os.path.abspath("/app"))
    uvicorn.run("config.asgi:application", host="0.0.0.0", reload=True)
