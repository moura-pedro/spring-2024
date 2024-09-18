"""
File: closest.py
Code inpired by T. Cormen's Intro to Algo. Chp 33, pg 1039
"""

import math
import sys

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def find_closest_pair(points):
    def find_closest_recursive(px, py):
        n = len(px)
        if n <= 3:
            return min(calculate_distance(px[i], px[j]) for i in range(n) for j in range(i + 1, n))

        mid = n // 2
        qx = px[:mid]
        rx = px[mid:]
        qy = sort_points_by_y(qx)
        ry = sort_points_by_y(rx)

        left_distance = find_closest_recursive(qx, qy)
        right_distance = find_closest_recursive(rx, ry)

        delta = min(left_distance, right_distance)
        strip = [point for point in py if abs(float(point.x) - float(px[mid].x)) < delta]

        find_closest_in_strip(strip, delta)

        return delta


    def find_closest_in_strip(strip, d):
        for i in range(len(strip)):
            for j in range(i + 1, len(strip)):
                if float(strip[j].y) - float(strip[i].y) < d:
                    update_closest_pair(strip[i], strip[j])
                else:
                    break


    def sort_points_by_y(points):
        return sorted(points, key=lambda p: p.y)


    def calculate_distance(p1, p2):
        return math.sqrt((float(p1.x) - float(p2.x))**2 + (float(p1.y) - float(p2.y))**2)


    def update_closest_pair(candidate1, candidate2):
        nonlocal min_distance
        distance = calculate_distance(candidate1, candidate2)
        if distance < min_distance:
            min_distance = distance
    
    points.sort(key=lambda p: p.x)
    min_distance = float('inf')
    find_closest_recursive(points, sort_points_by_y(points))
    return min_distance


def main():
    points_file = sys.argv[1]
    output_file = sys.argv[2]

    points = []
    with open(points_file, "r") as file:
        for line in file:
            x, y = line.split()
            points.append(Point(float(x), float(y)))

    result = str(find_closest_pair(points))
    with open(output_file, "w") as file:
        file.write("The closest pair of points is " + result)

main()