#!/usr/bin/env python3

import os

import random


# Standard division Euclid GCD is quite slow (fast enough that we'll get an output
# in a reasonable time, but still). Let's use Python's implementation. Hopefully,
# it's the Binary variant of the Euclid's algorithm or is otherwise more optimized.
from math import gcd


def load_message(ciphered, idx):
    folder = "ciphered" if ciphered else "plaintexts"
    with open(folder + "/test{}.txt".format(idx), "rb") as f:
        raw_data = f.read()
    return int.from_bytes(raw_data, "big")


c1 = load_message(True, 1)
c2 = load_message(True, 2)

m1 = load_message(False, 1)
m2 = load_message(False, 2)


# We know that m1**e = c1 (mod n) means that m1**e = k1*n + c1.
# Similarly, m2**e = k2*n + c2.
# Thus, k1*n = m1**e - c1 and k2*n = m2**e - c2.
# Consequently, n | gcd(m1**e - c1, m2**e - c2). In the best of cases,
# gcd(m1**e - c1, m2**e - c2) = n directly (k1 and k2 are coprime). Otherwise
# we would have n multiplied by a (hopefully) small enough integer
# e is typically chosen to be 65537

e = 65537

print("computing LHS")
lhs1 = m1**e - c1
print("computing RHS")
lhs2 = m2**e - c2
print("computing GCD")
print(gcd(lhs1, lhs2))

# technically we should try to figure out if n is multiplied by some integer.
# If this doesn't work out, we'd need to try to divide the previous result
# by a bunch of small integers to isolate n (we could try the primes up
# to 2**32 for instance).

