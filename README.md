# CS486 Assignment 1
# Author: Isaac Chang

# Question 1 Instructions:

- The program is set up to currently to run through only the 16 cities case for all 10 test cases.
- Results of the test (path, nodes generated, time) will be printed to stdout after each test case is ran.
- Uncomment out line 49 if you want to view the path on a plot using matplotlib
- Feel free to modify the `calc_heur` function if you want to try the zero heuristic
### - Note that some of the test cases may takeup to 1 to 2 minutes. (The first test case of 16 cities takes about 70s)

To Run:

- `cd src`
- `python q1.py`

# Question 2 Instructions:

- The program is set up to run using the backtrack + forward check + heuristic version of the solver
  through all 72 initial condition cases through all 10 test cases each.
- In order to run using the other versions of the solver uncomment out either line:
  35: Backtrack
  36: Backtrack + Forward Check
  37: Backtrack + Forward Check + Heuristic
- Results of the test (print out of the grid, number of variable assignments) will be printed after each test case is ran.
- Note that this version of the solver (backtrack + forward check + heuristic) does take a few seconds to run
  regardless of the numeber of initial values.
  
To Run:
  
- `cd src`
- `python q2.py`
