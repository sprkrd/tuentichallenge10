#!/usr/bin/env python3

import re

def preprocess_data():
    COMPILED_RE = re.compile("[^abcdefghijklmnñopqrstuvwxyzáéíóúü]")
    word_frequency = {}
    with open("pg17013.txt", "r") as f:
        for line in f:
            line_re = COMPILED_RE.sub(" ", line.lower())
            for word in line_re.split():
                if len(word) >= 3:
                    word_frequency[word] = word_frequency.get(word, 0) + 1
    sorted_words = sorted(word_frequency.keys(), key=lambda w: (-word_frequency[w], w))
    word_rank = {}
    for rank, word in enumerate(sorted_words, 1):
        word_rank[word] = rank
    return word_frequency, word_rank, sorted_words


WORD_FREQUENCY, WORD_RANK, SORTED_WORDS = preprocess_data()

N = int(input())

for i in range(1, N+1):
    print("Case #{}: ".format(i), end="")
    W = input()
    try:
        R = int(W)
        word = SORTED_WORDS[R-1]
        word_frequency = WORD_FREQUENCY[word]
        print(word, word_frequency)
    except ValueError: # it's a word
        word_frequency = WORD_FREQUENCY[W]
        word_rank = WORD_RANK[W]
        print(word_frequency, "#{}".format(word_rank))


