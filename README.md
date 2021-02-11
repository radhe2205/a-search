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

#### Further optimising the solution.
On running above program with BFS on 50 x 50 board, it took very high time, to find shortest path.
To fix this, explored the two way search approach. This approach was able to find the path very
quickly in less 5 seconds.

To implement this, 2 queues were used, one for forward search and one for reverse search.
Once the forward or reverse search reaches a node that has already been found by other search, we stop the algorithm
& return the path.

Another change that it needed was to convert the path of reverse search. For example if reverse search took left to reach 
a node; from source to target node, agent will have to take right.


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


## Part 2
#### Functional issues with the provided program
The issue with provided program is that it doesnt check if two agents placed can see each other.
Successor function is returning wrong successor states, which is resulting in wrong output.
On fixing successor function, the output given by the program is correct.

#### Algorithm analysis
Provided algorithm, generates successors of the initial state S_i, which have 
1 more p(agent) on the board than the current state. Similarly we see that 
each successor state will have more p's as we follow successors.
We can say that to place 8 p's we will have to go 8 node deep.

This means that to find any solution, we will have to go 8 node deeper into exploration.
If we choose a BFS exploration, we will explore all the states at depth 7.
that would mean we will be exploring almost b^7 states, where b is
average branching factor.

DFS exploration, on the other hand, traverses depths before exploring
breadths. This way DFS exploration is faster than BFS exploration for this
exploration. 

Since we only need to find the solution, which is placing n p's on
the board, and there is no difference between two solution, the requirement
for optimality is not there. So DFS exploration suits this problem better. DFS exploration
also keeps the memory usage at the minimum compared to BFS exploration, as it keeps less
states in the fringe.

The appropriate data structure for this would be **Stack** in that case.


#### Optimisations
The count_pichu function calculates the number of p on board everytime.
Since for nxm board, there are n.m cells to examine, this causes a lot of extra calculations.
To solve this, as we know in each successor state, there will be one more p, we can store the count
of p's along with each board state. When we generate states with successor function, we dont have
to re-calculate the number of p's, as we can just add 1 to the current count of p's.

So along with state, we also store the count of p. This also doesnt require huge memory as
we are already storing mxn integers in fringe, this is just one extra integer.


#### Other data structures and result comparisons
To validate the hypothesis regarding choice of data structure, I used following data structures.
* list with queue operations (provided)
* list with stack operations (instead of appending, adding to the front of list)
* PriorityQueue with most #p
* SimpleQueue

Following observations were captured.
1) List with queue operations became very slow deep into exploration. On analysing it was found that
list with queue operations using -> `a = [node] + a`, is creating another
   similar list, and is not reusing the same list. Which is causing huge delays in 
   insertions. Moreover, the fringe size is also high because of BFS algorithm.
   This caused even higher delays in insertions, because of cloning of orignal fringe everytime.
2) SimpleQueue was used to compare the results with _list with queue_. So _list with queue_ was compared
   with SimpleQueue. _list with queue_ performed much faster than _SimpleQueue_. As pointed
   out earlier _list with queue_ suffered heavy delay in insertions so it was slow.
3) **[IMP]** PriorityQueue with most #p being the highest priority was also tested. On implementation
it was found that PriorityQueue with most #p is very similar to DFS algorithm.
   This is because, in DFS algorithm we always choose the node at highest depth. For this problem 
   being at highest depth also means that it will have high number of p's, as established in
   **Algorithm Analysis** section earlier.
   
A counter was placed inside the loop to know the total number of states explored.
Maximum fringe size was also captured to find out the maximum fringe size reached during
a run.

The results are added in a separate CSV file named "A0 DS results.csv" in same directory. Link: //TODO


#### Analysing results comparison b/w _PriorityQueue with max p's_ & _list with stack_
As stated in pt.3 earlier, PriorityQueue and DFS(using stack) algo are basically the same. However on running
these algorithms on same problems, the #states explored were different. This was counter
intuitive, on investigation it was found that when a state S is explored and successor states = (S1, S2,... ,Sn)
are generated, the DFS algorithm picks the Sn next for exploration. While PriorityQueue algorithm picks
the S1 to explore next. Because depths of all of the states S1, S2, S3, ..., Sn are same, the sequence is maintained.

This results in different numbers for both the data structures.

### Solving Extra credit problem and incorporating the learning into part 2
The other part of problem requires us to place maximum possible p's on the board.
Following observations can be made.
* We will have to explore all the states and not just at depth = p.
* Since we have to explore all the states, it is again better to not choose BFS algorithm, 
  because we will anyway be exploring all the states, it is better to keep the memory used to a minimum.
  
A separate implementation was written to solve extra credit problem, to keep the code clean.
Anytime a max p count was reached, it was stored in a separate variable. On exploring all states, 
whatever max was reached was returned.

The program returned correct output, however it was a bit slow for larger boards.
Other approaches like 
* filling the board with p's and one by one removing them.
* counting the number of cells a 'p' affects and prioritizing the p's that should be placed first.

were thought of, but as these algo's required significant change, were discarded.

Since it is difficult to circumvent exploring all states, reducing the number of states to explore would make 
algorithm faster overall.

#### Reducing the number of explored states.
To reduce the number of states, we need to intellently discard some of the successor states.
Lets assume a state has 3 p's named p1, p2, p3 (here p1, p2 and p3 correspond to particular cell). This state is successor state of the board 
with only p1, p2 OR only p2, p3 OR only p1, p3. So during exploration, as we can not store whether 
a state has been visited, we are inadvertently exploring the state with p1, p2, p3 three times. If we could
introduce the sequence in placement of p1, p2 and p3, that might solve the problem.
What it means is that, we should force the algo to no place p1 if p2 is already present and likewise
to not place p2 if p3 is already present. This way; p1, p2, p3 will be successor state of board with only p1 and p2 present.

This can be accomplished if we store the last position of p present on board and in the successor function,
we only return the states which place the p after last placed p and not before that.

This results in significant improvements. For slightly larger boards, this returns results in acceptable time.

As extra credit algo is very similar to nQueen, tried solving nQueen too, returned results quite fast. It explored 1651 states.

#### Reducing the states in original part 2 problem.
As original part-2 problem can also benefit from reducing the number of states, 
the implementation was changed to sequence the placement of p's on the board. In BFS exploration, where it was exploring around
~65k - 200k states, with new sequencing in states, almost 2k-15k states were explored for boards of varying size.

#### [IMP]Significantly fast PriorityQueue data structure in part 2.
While running the problem with different data structures on different boards. It was realised
that program with PriorityQueue runs significantly faster compared to program with Stack, for every board. 
For various boards of 12x12, program with PriorityQueue explored around 500-600 states. While program with Stack explored around
5k - 30k states.

On diving deeper, found that when all the states have same number of p's, it selects the state with p
having lowest position. It is also intuitive, that a state with p's tightly packed has more chances of finding a solution.
So the PriorityQueue algorithm incidently chose the state which had all the p's tightly packed. In other words,
when 2 states have same number of p's, we choose a state which limits the p in minimum possible cell number(i * m + j, for cell i,j and n * m board)

_Note: edge cases when some p's are already present on the initial board were also handled._

### Problem abstractions
#### State space:
State space is the current state of the board. So the configuration of the board itself is a state.
for m x n board, we can place ".Xp@" at any cell. So total possible states on a board of size m*n
is = 4^(m*n)

#### Initial state:
Initial state of the board is read from the file.

#### Goal state:
Goal state of the board is reached when #p on the board = desired number.

#### Successor function:
Successor function of the final model for a state S is
successor(S) = (replace any one "." with "p" where p is not facing other p directly & p is placed after last located p in state S)

#### Cost:
Cost of each move, to go to successor state is same = 1. The cost function is uniform.


Reference:
Program shared by Jugal shah was used to generate the boards of varying size.