"""
File: sharenames.py
Midterm 01
Author: Pedro Moura #903962609
Feb 27, 2024
"""

import sys

input_file = open(sys.argv[1], "r")
output_file = open(sys.argv[2], "w")

name_dict = dict()

with input_file as file:
    lines = file.readlines()
    for name in lines:
        parts = name.strip().split()

        for part in parts:
            if part not in name_dict:
                name_dict[part] = []
                
            if name.strip() not in name_dict[part]:
                name_dict[part].append(name.strip())

for part in name_dict:
    name_dict[part].sort()

with output_file as file:
    for part in sorted(name_dict.keys()):
        if len(name_dict[part]) > 1:
            file.write(f"{part}:\n")
            for name in name_dict[part]:
                file.write(f"  {name}\n")
