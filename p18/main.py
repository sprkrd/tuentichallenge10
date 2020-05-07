#!/usr/bin/env python3


from tqdm import tqdm

import multiprocessing as mp

import sys
sys.setrecursionlimit(10000)


inf = float("inf")

def is_literal(c):
    return c not in "[],\n"


class EditCost:

    def __init__(self, data):
        self.data = data
        self.cache = {}

    def __call__(self, i=0, b=False, c=0, d=True, e=True):
        """
        b : at least one comma in current line, or no more lines (for ESC)
        c : # open brackets (for LOLMAO)
        d : literal may follow (for LOLMAO)
        e : can open new bracket (for LOLMAO)
        """
        if (i,b,c,d,e) not in self.cache:
            data = self.data
            if c < 0 or c > (len(data)-i):
                value = inf
            elif i == len(data):
                value = 0 if b and c == 0 else inf
            else:
                cost_lit = inf if not d else (not is_literal(data[i])) + self(i+1,b,c,True,False)
                cost_br = inf if (not b or not d) else ((data[i] != "\n") + self(i+1,False,c,True,False))
                cost_comma = inf if c == 0 else ((data[i] != ",") + self(i+1,True,c,True,True))
                cost_open = inf if not e else (data[i] != "[") + self(i+1,b,c+1,True,True)
                cost_close = (data[i] != "]") + self(i+1,b,c-1,False,False)
                value = min(cost_lit, cost_br, cost_comma, cost_open, cost_close)
            self.cache[(i,b,c,d,e)] = value
        return self.cache[(i,b,c,d,e)]


def solve_task(task):
    solution = EditCost(task[1])()
    if solution == inf:
        solution = "IMPOSSIBLE"
    return (task[0], solution)


tasks = []


C = int(input())
for i in range(1,C+1):
    L = int(input())
    data = ""
    for l in range(L):
        data += input()
        if l < L-1:
            data += "\n"
    tasks.append((i, data))


with mp.Pool(processes=6) as p:
    solutions = []
    for sol in tqdm(p.imap_unordered(solve_task, tasks)):
        solutions.append(sol)


solutions.sort()
for i,sol in solutions:
    print("Case #{}: {}".format(i, sol))


