#!/usr/bin/env python3

import re
from socket import socket, AF_INET, SOCK_STREAM
from collections import deque

HOST = "52.49.91.111"
PORT = 2003
MAP_LINE_RE = re.compile(r"[.#KP]{5}")
KNIGHT_NEIGHBORS = {
        "2u1l": (-2,-1),
        "1u2l": (-1,-2),
        "1d2l": (1,-2),
        "2d1l": (2,-1),
        "2d1r": (2,1),
        "1d2r": (1,2),
        "1u2r": (-1,2),
        "2u1r": (-2,1)
}


def next_map(f):
    print("Reading next map")
    next_map = []
    while len(next_map) < 5:
        line = next(f).strip()
        if MAP_LINE_RE.match(line):
            next_map.append(line)
        else:
            print(line)
    return next_map


def find_coordinates(m, x, offset=(0,0)):
    all_coords = []
    for i,row in enumerate(m):
        for j, tile in enumerate(row):
            if row[j] == x:
                all_coords.append((i+offset[0]-2, j+offset[1]-2))
    return all_coords


def get_neighbors(loc, obstacles):
    neighbors = []
    for direction, (inc_i, inc_j) in KNIGHT_NEIGHBORS.items():
        neighbor = (loc[0]+inc_i, loc[1]+inc_j)
        if neighbor not in obstacles:
            neighbors.append((direction, neighbor))
    return neighbors


def get_next_cell(loc, direction):
    vec = KNIGHT_NEIGHBORS[direction]
    return (loc[0]+vec[0], loc[1]+vec[1])


def shortest_path(init, dest, obstacles):
    traceback = {init: None}
    q = deque()
    q.append(init)
    while q and dest not in traceback:
        loc = q.popleft()
        for direction, neighbor in get_neighbors(loc, obstacles):
            if neighbor not in traceback:
                traceback[neighbor] = (direction, loc)
                q.append(neighbor)
    if dest in traceback:
        path = []
        curr = dest
        while curr != init:
            direction, previous = traceback[curr]
            path.append(direction)
            curr = previous
        path.reverse()
        return path
    else:
        return None
            

# the algorithm can be largely optimized (e.g. A*, avoiding computing shortest
# path if previous path is still valid, etc.), but this is good enough to get
# the solution in a couple of minutes at most.


with socket(AF_INET, SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    sfile = s.makefile("r")
    current_map = next_map(sfile)
    print("\n".join(current_map))
    at = (0,0)
    obstacles = set()
    princess_at,*_ = find_coordinates(current_map, "P")
    obstacles.update(find_coordinates(current_map, "#", at))
    first_iteration = True
    while at != princess_at:
        if not first_iteration:
            current_map = next_map(sfile)
            obstacles.update(find_coordinates(current_map, "#", at))
            # print("\n".join(current_map))
        path = shortest_path(at, princess_at, obstacles)
        print("current shortest path: ", path)
        chosen_dir = path[0]
        at_after = get_next_cell(at, path[0])
        print("Move {}, from {} to {}".format(chosen_dir, at, at_after))
        at = at_after
        s.send(chosen_dir.encode("ascii")+b"\n")
        first_iteration = False

    for l in sfile:
        print(l)


