"""
File: towers.py
Midterm 01
Author: Pedro Moura #903962609
Feb 29, 2024
"""

import sys

RED = "Red"
BLUE = "Blue"

input_file = open(sys.argv[1], "r")
output_file = open(sys.argv[2], "w")

def double_towers_of_hanoi(A, B, C, n, color):
    other = BLUE if RED else RED
    if n == 1:
        moves.append(f"Move {color} disc {n} from {A} to {C}")
        moves.append(f"Move {other} disc {n} from {A} to {B}")
        moves.append(f"Move {color} disc {n} from {C} to {B}")
    else:
        # Not quite right
        # TODO: fix color bug for input n>2
        double_towers_of_hanoi(A, C, B, n - 1, color)
        moves.append(f"Move {color} disc {n} from {A} to {B} asd")
        moves.append(f"Move {other} disc {n} from {A} to {B} ASD")
        double_towers_of_hanoi(C, B, A, n - 1, color)


def split_problem(A, B, C, n, color):
    other = BLUE if RED else RED
    if n == 1:
        moves.append(f"Move {color} disc {n} from {A} to {B}")
        moves.append(f"Move {other} disc {n} from {A} to {C}")
        
    else:
        double_towers_of_hanoi(A, C, B, n - 1, color)  
        moves.append(f"Move {color} disc {n} from {A} to {B}")  
        double_towers_of_hanoi(C, B, A, n - 1, color)  
        moves.append(f"Move {other} disc {n} from {A} to {C}")  
        double_towers_of_hanoi(B, A, C, n - 1, color)  
        split_problem(A, B, C, n - 1, color)

moves = []
n = int(input_file.readline())

split_problem('Peg 1', 'Peg 3', 'Peg 2', n, RED)

output_file.write(str(n) + "\n")
for move in moves:
    output_file.write(move + "\n")