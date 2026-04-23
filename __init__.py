"""Module-level entry point for the add-on into Anki 2.1"""

import os
import sys

# Add the "lib" directory to the Python path so anki can find our dependencies.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))

from .main import main

main()
