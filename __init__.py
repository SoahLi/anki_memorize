"""Module-level entry point for the add-on into Anki 2.1"""

import os
import sys

addon_root = os.path.dirname(__file__)
if addon_root not in sys.path:
    sys.path.insert(0, addon_root)

# Add the "lib" directory to the Python path so anki can find our dependencies.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))


from . import __main__

__main__.main(True)
