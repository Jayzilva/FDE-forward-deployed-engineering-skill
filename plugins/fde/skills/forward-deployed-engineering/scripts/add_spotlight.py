#!/usr/bin/env python3
"""Deprecated name. Use add_fspark.py: it adds the FSPARK feedback tour."""
import pathlib, runpy, sys
sys.argv[0] = str(pathlib.Path(__file__).with_name("add_fspark.py"))
runpy.run_path(sys.argv[0], run_name="__main__")
