#!/usr/local/bin/python3
#
# arrange_pichus.py : arrange agents on a grid, avoiding conflicts
#
# Submitted by : radverma
#
# Based on skeleton code in CSCI B551, Spring 2021
#


import sys
import time

# Parse the map from a given filename
def parse_map(filename):
	with open(filename, "r") as f:
		return [[char for char in line] for line in f.read().rstrip("\n").split("\n")]

# Count total # of pichus on board
def count_pichus(board):
    return sum([ row.count('p') for row in board ] )

# Return a string with the board rendered in a human-pichuly format
def printable_board(board):
    return "\n".join([ "".join(row) for row in board])

# Add a pichu to the board at the given position, and return a new board (doesn't change original)
def add_pichu(board, row, col):
    return board[0:row] + [board[row][0:col] + ['p',] + board[row][col+1:]] + board[row+1:]

def add_pichu_q(board, row, col):
    return (board[0:row] + [board[row][0:col] + ['q',] + board[row][col+1:]] + board[row+1:], get_cell_number(row, col, len(board[0])))

def is_pichus_hidden_on_board(board, row, col):
    return is_pichus_hidden_in_line([row[col] for row in board], row) and is_pichus_hidden_in_line(board[row][:], col)

def is_pichus_hidden_on_board2(board, row, col):
    hidden = is_pichus_hidden_in_line([row[col] for row in board], row) and is_pichus_hidden_in_line(board[row][:], col)
    if not hidden:
        return False
    diagonals = get_diagonals_with_pivot(board, row, col)

    return is_pichus_hidden_in_line(diagonals[0][0], diagonals[0][1]) and is_pichus_hidden_in_line(diagonals[1][0], diagonals[1][1])

def get_cell_number(row, col, column_count):
    if row < 0 or col < 0:
        return -1
    return row * column_count + col

def get_diagonals_with_pivot(board, row, col):
    line1 = []
    line2 = []
    for i in range(len(board)):
        col1 = col + (i - row)
        col2 = col + (row - i)
        if (i == row):
            pivot1 = len(line1)
            pivot2 = len(line2)
        if (col1 >= 0 and col1 < len(board[0])):
            line1.append(board[i][col1])
        if (col2 >= 0 and col2 < len(board[0])):
            line2.append(board[i][col2])

    return [(line1, pivot1), (line2, pivot2)]

def is_pichus_hidden_in_line(line, index):
    i = index - 1
    while(i >= 0):
        if line[i] in 'pq':
            return False
        if line[i] in '@X':
            break
        i = i-1

    i = index + 1

    while(i < len(line)):
        if line[i] in 'pq':
            return False
        if line[i] in '@X':
            return True
        i = i+1

    return True

# Get list of successors of given board state
def successors(board, max_pichus_pos):
    return [add_pichu_q(board, r, c) for r in range(max(int(max_pichus_pos / len(board[0])), 0), len(board)) for c in range(0, len(board[0]))
            if board[r][c] == '.' and
            is_pichus_hidden_on_board(board, r, c)
            and max_pichus_pos < get_cell_number(r, c, len(board[0]))]

# get successors for diagonally impacted agents
def successors_diagonal(board, max_pichus_pos):
    return [add_pichu_q(board, r, c) for r in range(max(int(max_pichus_pos / len(board[0])), 0), len(board)) for c in range(0, len(board[0]))
            if board[r][c] == '.' and
            is_pichus_hidden_on_board2(board, r, c) and
            max_pichus_pos <= get_cell_number(r, c, len(board[0]))]

# check if board is a goal state
def is_goal(board, k):
    return count_pichus(board) == k

def get_highest_pichus_cell(board):
    return max([get_cell_number(i,j, len(board[0])) for i, row in enumerate(board) for j, col in enumerate(row) if col == 'q'] + [(-1)])

from queue import Queue, PriorityQueue, LifoQueue


class StateObject:
    def __init__(self, object, priority):
        self.data = object
        self.priority = priority
    def __lt__(self, other):
        return self.priority < other.priority

def get_fringe(algo):
    if algo in ("list_stack", "list_queue"):
        return []
    if algo in ("pq_dfs"):
        return PriorityQueue()
    if algo == "queue":
        return Queue()
    if algo == "lifo_q_stack":
        return LifoQueue()

def insert_in_fringe(fringe, item, algo):
    if algo == "list_stack":
        fringe.append(item)
    if algo == "list_queue":
        fringe = [item] + fringe
    if algo == "queue":
        fringe.put(item)
    if algo == "lifo_q_stack":
        fringe.put(item)
    if algo == "pq_dfs":
        if item[1] == 0: # When there are no pichus on board
            priority = 0
        else:
            board = item[0] # reverse priority is decimal, x.y, where x is #p and y is proportional to max pichus position
            reverse_priority = item[1] + (1-item[2] / (len(board[0]) * len(board)))
            priority = 1 / reverse_priority
        fringe.put((StateObject(item, priority)))
    return fringe

def replace_q_p(board):
    for i,j in [(r,c) for r in range(len(board)) for c in range(len(board[0])) if board[r][c] == 'q']:
        board[i][j] = 'p'

def get_fringe_item(fringe, algo):
    if algo in ("list_stack", "list_queue"):
        return fringe.pop()
    if algo in ("pq_dfs"):
        return fringe.get().data
    if algo in ("queue", "lifo_q_stack"):
        return fringe.get()

def is_fringe_empty(fringe, algo):
    if algo in ("list_stack", "list_queue"):
        return len(fringe) == 0
    if algo in ("queue", "pq_dfs", "lifo_q_stack"):
        return fringe.empty()

def solve_diagonal(initial_board):

    max_pichus = count_pichus(initial_board)
    max_pichus_board = initial_board

    algo = "list_stack"

    fringe = get_fringe(algo)

    max_pichus_pos = get_highest_pichus_cell(initial_board)

    fringe = insert_in_fringe(fringe, (initial_board, count_pichus(initial_board), max_pichus_pos), algo)

    while not is_fringe_empty(fringe, algo):

        (board, pichus_count, max_pichus_pos) = get_fringe_item(fringe, algo)

        for (s, max_pichus_pos) in successors_diagonal(board, max_pichus_pos):
            if pichus_count + 1 > max_pichus:
                max_pichus_board = s
                max_pichus = pichus_count + 1

            item = (s, pichus_count + 1, max_pichus_pos)

            fringe = insert_in_fringe(fringe, item, algo)

    replace_q_p(max_pichus_board)
    return (max_pichus_board,True)

# Arrange agents on the map
#
# This function MUST take two parameters as input -- the house map and the value k --
# and return a tuple of the form (new_map, success), where:
# - new_map is a new version of the map with k agents,
# - success is True if a solution was found, and False otherwise.
#
def solve(initial_board, k):
    if k == 0:
        return solve_diagonal(initial_board)

    solution = None

    algo = "pq_dfs"
    fringe = get_fringe(algo)
    max_pichus_pos = get_highest_pichus_cell(initial_board)

    fringe = insert_in_fringe(fringe, (initial_board, count_pichus(initial_board), max_pichus_pos), algo)

    while not is_fringe_empty(fringe, algo):
        (board, pichus_count, max_pichus_pos) = get_fringe_item(fringe, algo)
        for (s, max_pichus_pos) in successors( board, max_pichus_pos ):
            if pichus_count + 1 == k:
                solution = (s,True)
                break

            fringe = insert_in_fringe(fringe, ((s, pichus_count + 1, max_pichus_pos)), algo)

        if solution is not None:
            break

    if solution is not None:
        replace_q_p(solution[0])
        return solution

    return ([],False)


# Main Function
if __name__ == "__main__":
    house_map=parse_map(sys.argv[1])

    # This is K, the number of agents
    k = int(sys.argv[2])
    print ("Starting from initial board:\n" + printable_board(house_map) + "\n\nLooking for solution...\n")
    (newboard, success) = solve(house_map, k)
    print ("Here's what we found:")
    print (printable_board(newboard) if success else "None")
