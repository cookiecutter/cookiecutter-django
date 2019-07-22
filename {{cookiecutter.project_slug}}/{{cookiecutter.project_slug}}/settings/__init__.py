try:
    from .dev import *  # NOQA
except ImportError:
    from .prod import *  # NOQA
