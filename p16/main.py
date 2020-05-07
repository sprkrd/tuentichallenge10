#!/usr/bin/env python3


from multiprocessing import Pool
from pulp import *
from sys import stderr


# Let's solve this as a LP. 



class Group:
    def __init__(self, group_id, E, available_floors):
        self.group_id = group_id
        self.E = E
        self.available_floors = available_floors


def solve(task):
    task_id, F, groups = task
    prob = LpProblem("tuentichallengeX-16", LpMinimize)
    variables_per_floor = [[] for _ in range(F)]
    variables_per_group = [[] for _ in groups]
    for g in groups:
        for f in g.available_floors:
            variable = LpVariable("WC_{}_{}".format(f, g), lowBound=0, cat="Integer")
            variables_per_floor[f].append(variable)
            variables_per_group[g.group_id].append(variable)
    M = LpVariable("M", 0) # not necessary to force integrality here
    prob += M, "min_wc"
    for f in range(F):
        prob += lpSum(variables_per_floor[f]) <= M, "max_wc_{}".format(f)
    for g in groups:
        prob += lpSum(variables_per_group[g.group_id]) >= g.E, "enough_wc_{}".format(g.group_id)
    prob.solve()
    print("task {} solved!".format(task_id), file=stderr)
    # probably just casting to int is OK, but better safe than sorry (imagine if some result is 24.99999987...)
    return round(value(prob.objective))
        

C = int(input())

tasks = []

for i in range(1, C+1):
    F,G = map(int, input().split())
    groups = []
    for group_id in range(G):
        E,N = map(int, input().split())
        available_floors = list(map(int, input().split()))
        groups.append(Group(group_id, E, available_floors))
    tasks.append((i,F,groups))

with Pool() as p:
    solutions = list(p.map(solve, tasks))

for i in range(1, C+1):
    print("Case #{}: {}".format(i, solutions[i-1]))



