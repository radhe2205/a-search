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
#
# class StateObject:
#     col, row = -1
#     board = [[]]


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

def is_pichus_hidden_on_board(board, row, col):
    return is_pichus_hidden_in_line([row[col] for row in board], row) and is_pichus_hidden_in_line(board[row][:], col)

def is_pichus_hidden_on_board2(board, row, col):
    hidden = is_pichus_hidden_in_line([row[col] for row in board], row) and is_pichus_hidden_in_line(board[row][:], col)
    if not hidden:
        return False
    diagonals = get_diagonals_with_pivot(board, row, col)

    return is_pichus_hidden_in_line(diagonals[0][0], diagonals[0][1]) and is_pichus_hidden_in_line(diagonals[1][0], diagonals[1][1])

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
        if line[i] == 'p':
            return False
        if line[i] in '@X':
            break
        i = i-1

    i = index + 1

    while(i < len(line)):
        if line[i] == 'p':
            return False
        if line[i] in '@X':
            return True
        i = i+1

    return True

# Get list of successors of given board state
def successors(board):
    return [ add_pichu(board, r, c) for r in range(0, len(board)) for c in range(0,len(board[0])) if board[r][c] == '.' and is_pichus_hidden_on_board(board, r, c) ]

# get successors for diagonally impacted agents
def successors_diagonal(board):
    return [ add_pichu(board, r, c) for r in range(0, len(board)) for c in range(0,len(board[0])) if board[r][c] == '.' and is_pichus_hidden_on_board2(board, r, c) ]

# check if board is a goal state
def is_goal(board, k):
    return count_pichus(board) == k 

from queue import SimpleQueue, PriorityQueue, LifoQueue


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
        return SimpleQueue()
    if algo == "lifo_q_stack":
        return LifoQueue()

def insert_in_fringe(fringe, item, algo):
    if algo == "list_stack":
        fringe.append(item)
    if algo == "queue":
        fringe.put(item)
    if algo == "lifo_q_stack":
        fringe.put(item)
    if algo == "pq_dfs":
        if item[1] == 0:
            priority = 0
        else:
            priority = 1 / item[1]
        fringe.put((StateObject(item, priority)))

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

    state_count = 1
    max_fringe_size = 1
    fringe_size = 1
    total_insert_time = 0
    algo_start_time = time.process_time()

    algo = "list_queue"

    fringe = get_fringe(algo)

    if algo != "list_queue":
        insert_in_fringe(fringe, (initial_board, count_pichus(initial_board)), algo)
    else:
        fringe = [(initial_board, count_pichus(initial_board))]

    while not is_fringe_empty(fringe, algo):

        (board, pichus_count) = get_fringe_item(fringe, algo)
        fringe_size = fringe_size - 1

        for s in successors_diagonal(board):
            state_count = state_count + 1
            fringe_size = fringe_size + 1
            if fringe_size > max_fringe_size:
                max_fringe_size = fringe_size

            if pichus_count + 1 > max_pichus:
                max_pichus_board = s
                max_pichus = pichus_count + 1

            item = (s, pichus_count + 1)

            start_time = time.process_time()
            if algo != "list_queue":
                insert_in_fringe(fringe, item, algo)
            else:
                fringe = [item] + fringe
            total_insert_time = total_insert_time + (time.process_time() - start_time)

            if state_count % 1000 == 0:
                print("Avg time: " + str(total_insert_time / state_count))
                print("States count: " + str(state_count))
                print("max fringe size: " + str(max_fringe_size))
                print("pichus_count: " + str(pichus_count + 1))

    print("Algo: " + algo)
    print("States explored: " + str(state_count))
    print("Max Fringe size: " + str(max_fringe_size))
    print("total time in insert ops: " + str(total_insert_time))
    print("avg time in fringe inserts: " + str(total_insert_time / state_count))
    print("Total time taken by algo: " + str(time.process_time() - algo_start_time))

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

    state_count = 1
    max_fringe_size = 1
    fringe_size = 1
    total_insert_time = 0
    algo_start_time = time.process_time()

    algo = "list_stack"
    fringe = get_fringe(algo)

    solution = None

    if algo != "list_queue":
        insert_in_fringe(fringe, (initial_board, count_pichus(initial_board)), algo)
    else:
        fringe = [(initial_board, count_pichus(initial_board))]

    while not is_fringe_empty(fringe, algo):
        (board, pichus_count) = get_fringe_item(fringe, algo)
        fringe_size = fringe_size - 1

        for s in successors_diagonal( board ):
            state_count = state_count + 1
            if pichus_count + 1 == k:
                solution = (s,True)
                break

            fringe_size = fringe_size + 1
            if max_fringe_size < fringe_size:
                max_fringe_size = fringe_size

            start_time = time.process_time()

            if algo != "list_queue":
                insert_in_fringe(fringe, ((s, pichus_count + 1)), algo)
            else:
                fringe = [(s, pichus_count + 1)] + fringe

            if state_count % 1000 == 0:
                print("Avg time: " + str(total_insert_time / state_count))
                print("States count: " + str(state_count))
                print("max fringe size: " + str(max_fringe_size))
                print("pichus_count: " + str(pichus_count + 1))

            total_insert_time = total_insert_time + (time.process_time() - start_time)
        if solution is not None:
            break

    print("Algo: " + algo)
    print("States explored: " + str(state_count))
    print("Max Fringe size: " + str(max_fringe_size))
    print("total time in insert ops: " + str(total_insert_time))
    print("avg time in fringe inserts: " + str(total_insert_time/state_count))
    print("Total time taken by algo: " + str(time.process_time() - algo_start_time))

    if solution is not None:
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
