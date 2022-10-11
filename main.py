#!/usr/bin/env python3

"""
The main program to build LLVM snapshot packages in Copr.
"""

import sys

from src.llvm_snapshot_builder.cmd.util import get_action, build_main_parser

if __name__ == "__main__":
    sys.exit(0 if get_action(build_main_parser()).run() else 1)
