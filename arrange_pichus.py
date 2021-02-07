#!/usr/local/bin/python3
#
# arrange_pichus.py : arrange agents on a grid, avoiding conflicts
#
# Submitted by : radverma
#
# Based on skeleton code in CSCI B551, Spring 2021
#


import sys
from queue import PriorityQueue

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
    try:
        return is_pichus_hidden_in_line([row[col] for row in board], row) and is_pichus_hidden_in_line(board[row][:], col)
    except Exception as e:
        print(str(row) + ", " + str(col))
        raise e


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

# check if board is a goal state
def is_goal(board, k):
    return count_pichus(board) == k 


# Arrange agents on the map
#
# This function MUST take two parameters as input -- the house map and the value k --
# and return a tuple of the form (new_map, success), where:
# - new_map is a new version of the map with k agents,
# - success is True if a solution was found, and False otherwise.
#
def solve(initial_board, k):
    count = 1
    fringe = [(initial_board, count_pichus(initial_board))]
    while len(fringe) > 0:
        (board, pichus_count) = fringe.pop()
        for s in successors( board ):
            count = count + 1
            if pichus_count + 1 == k:
                print(count)
                return(s,True)
            fringe.append((s, pichus_count + 1))
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


