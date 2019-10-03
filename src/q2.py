"""
CS 486 Assignment 1 Question 2
Author: Isaac Chang
Date Sep 29, 2019
"""

import sys
import copy
import pdb

class SudokuSolution:

    def __init__(self):
        self.sudoku_problems_file = '../data/sudoku_problems/1/1.sd'

    def main(self):
        num_passed = 0

        for i in range(1,11):
            print 'started test case # ' + str(i)
            file_name = '../data/sudoku_problems/15/' + str(i) + '.sd'

            grid = self.read_in(file_name)
            #self.print_grid(grid)

            #pdb.set_trace()

            #res, num_var = self.solve_backtrack(grid)
            valid_nums_grid = self.generate_forward_check_bool_arr()
            #res, num_var = self.solve_backtrack_forward_check(grid, valid_nums_grid)
            res, num_var = self.solve_backtrack_forward_check_heuristic(grid, valid_nums_grid)

            #pdb.set_trace()

            if res:
                #self.print_grid(grid)
                print 'PASSED total number of variable assignments: ' + str(num_var)
                num_passed += 1
            else:
                print 'FAILED total number of variable assignments: ' + str(num_var)
    
        print 'Passed ' + str(num_passed) + '/10 Test Cases' 

    def solve_backtrack_forward_check_heuristic(self, grid, valid_nums_grid):
        num_var = 0

        coord = [0,0]
    
       # Instead of just the next empty cell, look for the most constrained cell
        if not self.find_most_constrained_cell(grid, coord):
            return True, num_var

        # Found valid empty coordinate
        row = coord[0]
        col = coord[1]

        new_range = []

        for i in range(9):
            if valid_nums_grid[row][col][i] == True:
                new_range.append(i+1)

        #pdb.set_trace()

        new_range_sorted_lcv = self.sort_range_lcv(grid, new_range, row, col)

        #pdb.set_trace()

        for val in new_range_sorted_lcv:
            num_var += 1

            if num_var > 10000:
                return False, num_var

            valid = self.not_in_subgrid(grid, row - row%3, col - col%3, val)
            valid &= self.not_in_row(grid, row, val)
            valid  &= self.not_in_column(grid, col, val)

            if valid:
                grid[row][col] = val

                new_valid_nums_grid = copy.deepcopy(valid_nums_grid)

                # Update forward checking boolean array
                for i in range(9):
                    new_valid_nums_grid[row][i][val-1] = False
                    new_valid_nums_grid[i][col][val-1] = False

                for i in range(3):
                    for j in range(3):
                        if row - row%3 + i == 1 and col - col%3 + j == 0:
                            new_valid_nums_grid[row - row%3 + i][col - col%3 + j][val-1] = False

                res, temp_num_var = self.solve_backtrack_forward_check_heuristic(grid, new_valid_nums_grid)
                
                num_var += temp_num_var

                # If valid assignment then return True up call stack
                if res:
                    return True, num_var
                
                # If invalid then reset and try next term
                grid[row][col] = 0

        # If went through all vals and still invalid then this possibility has failed
        return False, num_var

    def solve_backtrack_forward_check(self, grid, valid_nums_grid):
        num_var = 0

        coord = [0,0]

        if not self.find_next_empty_cell(grid, coord):
            return True, num_var

        # Found valid empty coordinate
        row = coord[0]
        col = coord[1]

        new_range = []

        for i in range(9):
            if valid_nums_grid[row][col][i] == True:
                new_range.append(i+1)

        for val in new_range:
            num_var += 1

            if num_var > 10000:
                return False, num_var

            valid = self.not_in_subgrid(grid, row - row%3, col - col%3, val)
            valid &= self.not_in_row(grid, row, val)
            valid  &= self.not_in_column(grid, col, val)

            if valid:
                grid[row][col] = val

                new_valid_nums_grid = copy.deepcopy(valid_nums_grid)

                # Update forward checking boolean array
                for i in range(9):
                    new_valid_nums_grid[row][i][val-1] = False
                    new_valid_nums_grid[i][col][val-1] = False

                for i in range(3):
                    for j in range(3):
                        if row - row%3 + i == 1 and col - col%3 + j == 0:
                            new_valid_nums_grid[row - row%3 + i][col - col%3 + j][val-1] = False

                res, temp_num_var = self.solve_backtrack_forward_check(grid, new_valid_nums_grid)
                
                num_var += temp_num_var

                # If valid assignment then return True up call stack
                if res:
                    return True, num_var
                
                # If invalid then reset and try next term
                grid[row][col] = 0

        # If went through all vals and still invalid then this possibility has failed
        return False, num_var

    def solve_backtrack(self, grid):
        num_var = 0

        coord = [0,0]

        if not self.find_next_empty_cell(grid, coord):
            return True, num_var

        # Found valid empty coordinate
        row = coord[0]
        col = coord[1]

        for val in range(1,10):
            num_var += 1

            if num_var > 10000:
                return False, num_var

            valid = self.not_in_subgrid(grid, row - row%3, col - col%3, val)
            valid &= self.not_in_row(grid, row, val)
            valid  &= self.not_in_column(grid, col, val)

            if valid:
                grid[row][col] = val
                res, temp_num_var = self.solve_backtrack(grid)
                num_var += temp_num_var

                # If valid assignmen then return True up call stack
                if res:
                    return True, num_var
                
                # If invalid then reset and try next term
                grid[row][col] = 0

        # If went through all vals and still invalid then this possibility has failed
        return False, num_var
       
    # Helper Functions -----

    def generate_forward_check_bool_arr(self):
        valid_nums_grid1 = [True] * 9
        valid_nums_grid2 = []
        valid_nums_grid3 = []

        for i in range(9):
            valid_nums_grid2.append(copy.deepcopy(valid_nums_grid1))
        for i in range(9):
            valid_nums_grid3.append(copy.deepcopy(valid_nums_grid2))

        return valid_nums_grid3

    def sort_range_lcv(self, grid, temp_new_range, row, col):
        new_range = temp_new_range[:]
        
        if len(new_range) == 1:
            return new_range
        
        range_possible_vals = {}

        for num in new_range:
            valid = self.not_in_subgrid(grid, row - row%3, col - col%3, num)
            valid &= self.not_in_row(grid, row, num)
            valid  &= self.not_in_column(grid, col, num)

            if valid:
                temp_grid = copy.deepcopy(grid)
                temp_grid[col][row] = num

                total_possible_vals = 0

                for i in range(9):
                    for j in range(9):
                        # For each empty cell aggregate all the possible assignable values
                        if temp_grid[i][j] == 0:
                            for val in range(1,10):
                                valid = self.not_in_subgrid(temp_grid, i - i%3,j - j%3, val)
                                valid &= self.not_in_row(temp_grid, i, val)
                                valid  &= self.not_in_column(temp_grid, j, val)

                                if valid:
                                    total_possible_vals += 1
                
                range_possible_vals[num] = total_possible_vals
            else:
                range_possible_vals[num] = sys.maxint

        range_possible_vals = sorted(range_possible_vals, key=range_possible_vals.get)
       
        return range_possible_vals

    def find_most_constrained_cell(self, grid, coord):
        min_num_possible_vals = 10
        min_possible_vals = [] 
        found_empty_cell = False

        for row in range(9):
            for col in range(9):
                if grid[row][col] == 0:
                    found_empty_cell = True
                    possible_vals = []
                    num_possible_vals = 0

                    for val in range(1,10):
                        valid = self.not_in_subgrid(grid, row - row%3, col - col%3, val)
                        valid &= self.not_in_row(grid, row, val)
                        valid  &= self.not_in_column(grid, col, val)
        
                        if valid:
                            possible_vals.append(val)
                            num_possible_vals += 1

                    if num_possible_vals < min_num_possible_vals:
                        min_num_possible_vals = num_possible_vals
                        min_possible_vals = possible_vals[:]
                        coord[0] = row
                        coord[1] = col
                    elif num_possible_vals == min_num_possible_vals:
                        temp_grid = copy.deepcopy(grid)

                        curr_total_possible_vals = 0

                        for val in possible_vals:
                            temp_grid[row][col] = val
                            curr_total_possible_vals += self.find_total_possible_values(temp_grid)
                            temp_grid[row][col] = 0

                        prev_total_possible_vals = 0

                        for val in min_possible_vals:
                            temp_grid[coord[0]][coord[1]] = val
                            prev_total_possible_vals += self.find_total_possible_values(temp_grid)
                            temp_grid[coord[0]][coord[1]] = 0

                        if curr_total_possible_vals < prev_total_possible_vals:
                            min_num_possible_vals = num_possible_vals
                            min_possible_vals = possible_vals[:]
                            coord[0] = row
                            coord[1] = col
        
        if found_empty_cell: 
            return True
        return False 

    def find_total_possible_values(self, grid):
        total_possible_vals = 0

        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    for val in range(1,10):
                        valid = self.not_in_subgrid(grid, i - i%3,j - j%3, val)
                        valid &= self.not_in_row(grid, i, val)
                        valid  &= self.not_in_column(grid, j, val)

                        if valid:
                            total_possible_vals += 1

        return total_possible_vals

    def find_next_empty_cell(self, grid, coord):
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    coord[0] = i
                    coord[1] = j
                    return True

        return False 

    def not_in_subgrid(self, grid, start_row, start_col, val):
        for i in range(3):
            for j in range(3):
                if grid[start_row+i][start_col+j] == val:
                    return False
        return True

    def not_in_row(self, grid, row, val):
        for i in range(9):
            if grid[row][i] == val:
                return False
        return True

    def not_in_column(self, grid, col, val):
        for i in range(9):
            if grid[i][col] == val:
                return  False
        return True

    # IO Functions -----

    def print_grid(self, grid):
        for row in grid:
            for val in row:
                print str(val),
            print '\n'

    def read_in(self, file_name):
        f = open(file_name)

        lines = list(f)
        lines = lines[:len(lines)-1]
        
        grid = []

        for line in lines:
            row = line.split()
            row = [int(val) for val in row]
            grid.append(row)

        return grid

if __name__ == '__main__':
    sol = SudokuSolution()
    sol.main()
