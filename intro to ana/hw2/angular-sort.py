"""
File: angular-sort.py
"""

import math
import sys
import timsort as ts

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.quadrant = self.find_quadrant(float(x), float(y))

    
    def find_quadrant(self, x, y):
        if x >= 0 and y >= 0:
            return 1.0
        elif x <= 0 and y >= 0:
            return 2.0
        elif x <= 0 and y <= 0:
            return 3.0
        elif x >= 0 and y <= 0:
            return 4.0
        else:
            return 0


def main ():
    points = []

    input_file = sys.argv[1]
    with open(input_file, "r") as f:
        n = int(f.readline())
        for _ in range(n):
            x,y = f.readline().split() 
            points.append(Point(x,y))
        
    ts.timsort(points)
    
    sorted_file = sys.argv[2]
    with open(sorted_file, "w") as f:
        for point in points:
            f.write(f"{point.x} {point.y}\n")

    info_file = sys.argv[3]
    with open(info_file, "w") as f:
        f.write("Sorry Professor, but I failed you...")
            

main()