# from beartype.claw import beartype_this_package

# beartype_this_package()

"""Module-level entry point for the add-on into Anki 2.1"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))

from .main import main

main()
