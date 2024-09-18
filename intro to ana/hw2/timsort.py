"""
File: timsort.py
Inpired by https://www.educative.io/answers/what-is-timsort
"""

import math

minrun = 32
stack = []

def insertion_sort(arr, start, end):
    for i in range(start + 1, end + 1):
        temp = arr[i]
        j = i - 1
        while j >= start and angle_comparator(temp, arr[j]) < 0:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = temp
            

def merge(arr, l, m, r):
    len1, len2 = m - l + 1, r - m
    left, right = arr[l:l + len1], arr[m + 1:m + 1 + len2]

    i = j = 0
    k = l

    while i < len1 and j < len2:
        if angle_comparator(left[i], right[j]) <= 0:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1

    while i < len1:
        arr[k] = left[i]
        i += 1
        k += 1

    while j < len2:
        arr[k] = right[j]
        j += 1
        k += 1
        stack.append((l, len1 + len2))

def angle_comparator(p1, p2):
    if p1.quadrant != p2.quadrant:
        return (p1.quadrant > p2.quadrant) - (p1.quadrant < p2.quadrant)

    angle1 = math.atan2(float(p1.y), float(p1.x))
    angle2 = math.atan2(float(p2.y), float(p2.x))
    return (angle1 > angle2) - (angle1 < angle2)

def tim_sort_util(arr, n):
    for i in range(0, n, minrun):
        insertion_sort(arr, i, min((i + minrun - 1), n - 1))

    size = minrun
    while size < n:
        for left in range(0, n, 2 * size):
            mid = min((left + size - 1), n - 1)
            right = min((left + 2 * size - 1), n - 1)
            if mid < right:
                merge(arr, left, mid, right)
        size = 2 * size

def timsort(arr):
    tim_sort_util(arr, len(arr))
