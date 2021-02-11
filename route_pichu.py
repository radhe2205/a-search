#!/usr/local/bin/python3
#
# route_pichu.py : a maze solver
#
# Submitted by : [PUT YOUR NAME AND USERNAME HERE]
#
# Based on skeleton code provided in CSCI B551, Spring 2021.


import sys
import json

# Parse the map from a given filename
from queue import LifoQueue, Queue


def parse_map(filename):
    with open(filename, "r") as f:
        return [[char for char in line] for line in f.read().rstrip("\n").split("\n")]


# Return a string with the board rendered in a human/pichu-readable format
def printable_board(board):
    return "\n".join(["".join(row) for row in board])


# Check if a row,col index pair is on the map
def valid_index(pos, n, m):
    return 0 <= pos[0] < n and 0 <= pos[1] < m


# Find the possible moves from position (row, col)

def moves(map, row, col):
    moves = ((row + 1, col, "D"), (row - 1, col, "U"), (row, col - 1, 'L'), (row, col + 1, 'R'))

    # Return only moves that are within the board and legal (i.e. go through open space ".")
    return [move for move in moves if valid_index(move, len(map), len(map[0])) and (map[move[0]][move[1]] in ".@p")]

def get_reverse_path(path):
    reverse_path = ""
    reverse_key_map = {'D': 'U', 'U':'D', 'R':'L','L':'R'}
    for char in path[::-1]:
        reverse_path = reverse_path + reverse_key_map[char]
    return reverse_path

def get_actual_path_in_two_way_search(current_path, visited_path, is_forward_search):
    current_path = current_path if is_forward_search else get_reverse_path(current_path)
    visited_path = visited_path if not is_forward_search else get_reverse_path(visited_path)
    return current_path + visited_path if is_forward_search else visited_path + current_path

# Perform search on the map
#
# This function MUST take a single parameter as input -- the house map --
# and return a tuple of the form (move_count, move_string), where:
# - move_count is the number of moves required to navigate from start to finish, or -1
#    if no such route exists
# - move_string is a string indicating the path, consisting of U, L, R, and D characters
#    (for up, left, right, and down)
#
def search(house_map):
    forward_fringe = Queue()
    reverse_fringe = Queue()

    forward_search = True
    visited_cells = {}

    # Find pichu start position
    pichu_loc = [(row_i, col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if
                 house_map[row_i][col_i] == "p"][0]
    target_loc = [(row_i, col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if
                  house_map[row_i][col_i] == "@"][0]

    forward_fringe.put((pichu_loc, 0, ''))
    reverse_fringe.put((target_loc, 0, ''))

    while not forward_fringe.empty() and not reverse_fringe.empty():
        old_fringe = forward_fringe if forward_search else reverse_fringe
        new_fringe = Queue()

        while not old_fringe.empty():
            (curr_move, curr_dist, path) = old_fringe.get()

            visited_cells[(curr_move)] = (curr_dist, path, forward_search)

            if house_map[curr_move[0]][curr_move[1]] == "@" and forward_search:  # if Reached goal
                return (curr_dist, path)
            if house_map[curr_move[0]][curr_move[1]] == 'p' and not forward_search:
                return (curr_dist, path[::-1])

            for move in moves(house_map, *curr_move):
                if (move[0], move[1]) in visited_cells:
                    node = visited_cells[(move[0], move[1])]
                    if node[2] == forward_search:
                        continue
                    return (curr_dist + 1 + node[0], get_actual_path_in_two_way_search(path+move[2], node[1], forward_search))
                new_fringe.put((move[:2], curr_dist + 1, path + move[2]))

        if forward_search:
            forward_fringe = new_fringe
        else:
            reverse_fringe = new_fringe
        forward_search = not forward_search
    return (-1, "")


# Main Function
if __name__ == "__main__":
    house_map = parse_map(sys.argv[1])
    print("Routing in this board:\n" + printable_board(house_map) + "\n")
    print("Shhhh... quiet while I navigate!")
    solution = search(house_map)
    print("Here's the solution I found:")
    print(str(solution[0]) + " " + str(solution[1]))
