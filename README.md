### Problem 1: Finding the shortest path between agent and target.
### Scope
As this is a path finding problem, we can solve this 
using greedy approach or any other deterministic 
approach. However approach taken here will be, 
modelling the problem as a state exploration by 
agent, using abstraction.    

### Solution 

#### Solving Infinite loop: keep a track of visited states 
The given program runs into infinite loop when no 
solution exists. This is because the edges are
steps are bi-directional. So when the agent reaches
a dead end, it starts walking back,
still searching for target.

To solve this problem, we need to keep a record of
which all cells have been visited in exploration. 
Once we have reach a cell where all the further moves are visited, 
we will stop the exploration.  

#### Returning the path taken by agent

Another modification that we require is, 
to keep a record of all the steps leading upto current
state, as the program output requires for us to output
the steps taken by agent in "L|R|U|D" format.  
 
#### Conversion to BFS algorithm
We are required to find the shortest(optimal) path.
Given program is implemented in DFS fashion, 
which is not necessarily optimal. 
The implementation here needs to use BFS algorithm 
to find the shortest path.

_Note: as the cost to take a step is uniform, the BFS algorithm with stack will provide 
optimal solution, an implementation for priority queue is not required._  

### Abstraction
#### States
State at any given time will be the position of agent. For an m x n grid, any state 
will be of the form -> S = (i, j) where i ∈ [1,m] and j ∈ [1,n]

Total number of state = m*n

#### Successor function
Successor state of a state (i, j) returns a state (x, y) where x ∈ [i-1, i+1] 
& y ∈ [j-1, j+1] 

#### Cost function
For each step, the cost is uniform be it any of the move left, right, up, down. 
So cost for each successor state transition is uniform = 1

#### Initial state
Initial state is read from the file provided to the program as argument. Initial state
is S = (i, j), where i represents the row number and j represents column number of the 
cell of the agent.

#### Goal state
Goal state is reached when the agent reaches at the cell where the target is present.
In this case goal state is S = (i, j) where the target is present at i'th row and j'th
column


