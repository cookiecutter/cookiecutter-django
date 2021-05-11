import os
import sys

import uvicorn
from uvicorn.supervisors.watchgodreload import CustomWatcher


class WatchgodWatcher(CustomWatcher):
    def __init__(self, *args, **kwargs):
        self.ignored_dirs.update({"templates", "static", "compose"})
        super(WatchgodWatcher, self).__init__(*args, **kwargs)


uvicorn.supervisors.watchgodreload.CustomWatcher = WatchgodWatcher
if __name__ == "__main__":
    sys.path.insert(0, os.path.abspath("/app"))
    uvicorn.run("config.asgi:application", host="0.0.0.0", reload=True)
