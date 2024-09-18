"""
Filename: word-ladder.py
Author: Pedro Moura
Date: April 26, 2024
"""

import re

def process_dic(path):
    words = []

    with open(path, "r") as f:
        lines = f.readlines()

        for word in lines:
            if re.match("^[a-z]+$", word.strip()):
                words.append(word.strip())

    return words



def bfs(start, end, word_list):
    if end not in word_list:
        return 0
    
    queue = [(start, [start])]
    visited = set([start])
    wordSet = set(word_list)

    while queue:
        current_word, path = queue.pop(0)
        if current_word == end:
            return path

        for i in range(len(current_word)):
            alpha = set('abcdefghijklmnopqrstuvwxyz')

            for letter in alpha:
                next_word = current_word[:i] + letter + current_word[i + 1:]

                if next_word in wordSet and next_word not in visited:
                    visited.add(next_word)
                    queue.append((next_word, path + [next_word]))
    return []



def print_output(path):

    if len(path) == 0:
        print("Duh! Impossible.")
    else:
        print("Yay! A word ladder is possible.")
        for word in path:
            print(word)



def main():
    dictionary_path = "dictionary4"

    start = input()
    end = input()
    words = process_dic(dictionary_path)
 
    path = bfs(start, end, words)
    print_output(path)

main()
