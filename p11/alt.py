#!/usr/bin/env python3

class SumCount:

    def __init__(self, O):
        self.O = O
        self.cache = {}

    def __call__(self, x, i):
        if (x,i) not in self.cache:
            if x == 0:
                self.cache[(x,i)] = 1
            elif self.O[i] > x:
                self.cache[(x, i)] = 0
            else:
                self.cache[(x,i)] = self(x-self.O[i], i)
                if i < len(self.O)-1:
                    self.cache[(x,i)] += self(x, i+1)
        return self.cache[(x, i)]


T = int(input())
for case in range(1, T+1):
    X, *forbidden = map(int, input().split())
    O = set(range(1,X+1))
    for f in forbidden:
        O.discard(f)
    O = list(O)
    C = SumCount(O)
    S = C(X, 0) - 1
    print("Case #{}: {}".format(case, S))


