"""
CS 486 Assignment 1 Question 1
Author: Isaac Chang
Date: Sep 28, 2019
"""

import sys
import math
from Queue import PriorityQueue
import matplotlib.pyplot as plt
import time

import pdb

class Solution:

    def __init__(self):
        self.randTSP_file = '../data/randTSP/10/instance_1.txt'

    def main(self):
        print 'started ---------------'
        
        num_cities, g = self.read_in(self.randTSP_file)
        
        start_time = time.time()
        final_path, dist_travelled = self.a_star_tsp(num_cities, g, 'A')
        
        print 'results:'
        print 'time taken: ' + str(time.time() - start_time) + " second(s)" 
        print 'final path: ' + str(final_path)
        print 'distance travelled: ' + str(dist_travelled) + ' units'

        print 'ended ---------------'
        self.display_cities(g, final_path)

    def a_star_tsp(self, num_cities, g, s_city_name):
        s = g[s_city_name]

        q = PriorityQueue()

        q.put((0, [['A'], 0]))
    
        while not q.empty():
            temp  = q.get()[1]
            path = temp[0]
            prev_acc_cost = temp[1]
         
            #if len(path) == num_cities + 1:
                #pdb.set_trace()
            #    return path, prev_acc_cost

            if len(path) == num_cities:
                heur, acc_cost = self.calc_heur(g, path, s_city_name, s, prev_acc_cost)
                new_path = path[:]
                new_path.append(s_city_name)

                #q.put((heur, [new_path, acc_cost]))

                return new_path, acc_cost
            else:
                not_visited = set(path).symmetric_difference(set(g.keys()))

                for city in not_visited:
                    heur, acc_cost = self.calc_heur(g, path, city, s, prev_acc_cost)
                    new_path = path[:]
                    new_path.append(city)
                    q.put((heur, [new_path, acc_cost]))

                    #pdb.set_trace()

            #pdb.set_trace()
    
    # Heuristic Calculation Functions -----
    
    def calc_heur(self, g, path, next_city, s, prev_acc_cost):
        acc_cost = prev_acc_cost + self.eucl_dist(g[path[-1]], g[next_city])

        # Heuristic function 1
        h1 = self.eucl_dist(g[next_city], s)

        # Heuristic function 2
        # h2 = self.calc_min_next_dist(g, path, next_city) 

        # Heuristic function 3
        h3 = self.calc_mst_weight(g, path, next_city,)

        # Zero Heuristic function
        h0 = 0    

        f = acc_cost + h1 

        return f, acc_cost

    def calc_mst_weight(self, g, path, next_city):
        new_path = path[:]
        new_path.append(next_city)

        not_visited = set(new_path).symmetric_difference(set(g.keys()))
        not_visited = list(not_visited)
        # For looping back to A start node
        not_visited.append('A')

    def calc_min_next_dist(self, g, path, next_city):
        new_path = path[:]
        new_path.append(next_city)

        not_visited = set(new_path).symmetric_difference(set(g.keys()))

        if len(not_visited) == 0:
            return 0

        min_dist = sys.maxint

        for city in not_visited:
            dist = self.eucl_dist(g[path[-1]], g[city])
            min_dist = min(min_dist, dist)    

        return min_dist

    def calc_greedy(self, g, path, next_city):
        new_path = path[:]
        new_path.append(next_city)

        not_visited = set(new_path).symmetric_difference(set(g.keys()))

        greedy_dist = 0
        curr_city = path[-1]

        while(not_visited):
            min_dist = sys.maxint
            min_city = ''

            for city in not_visited:
                dist = self.eucl_dist(g[curr_city], g[city])
                if dist < min_dist:
                    min_city = city
                    min_dist = dist

            greedy_dist += min_dist
            curr_city = min_city
            not_visited.remove(min_city)

        return greedy_dist

    # Helper Functions -----

    def eucl_dist(self, c1, c2):
        x_delta = c1.x - c2.x
        y_delta = c1.y - c2.y

        dist = math.sqrt(x_delta ** 2 + y_delta ** 2)

        return dist

    def total_path_dist(self, g, path):
        dist = 0

        for i in range(len(path)-1):
            dist += self.eucl_dist(g[path[i]], g[path[i+1]])

        return dist
    
    # IO Functions -----

    def read_in(self, file_name):
        f = open(file_name)
        lines = list(f)

        g = dict()

        num_cities = int(lines[0])

        for i in range(1, len(lines)):
            city, x, y = lines[i].split()
            g[city] = self.City(int(x), int(y))

        return num_cities, g

    def display_cities(self, g, path):
        x_coords = []
        y_coords = []

        for point in path:
            x_coords.append(g[point].x)
            y_coords.append(g[point].y)

        fig, graph = plt.subplots()
        graph.scatter(x_coords, y_coords)

        for i, label in enumerate(path):
            graph.annotate(label, (x_coords[i], y_coords[i]))

        plt.show()

    # Helper Classes -----
    
    # A struct class to more easily store city coordinates
    class City:

        def __init__(self, x, y):
            self.x = x
            self.y = y

        def __str__(self):
            return "(X: {0}, Y: {1})".format(self.x, self.y)

    # A graph class which implements a MST weight finder
    # Implements a disjoint set to check for cycles in graph
    class MST_Graph:
        
        def __init__(self):
            self.graph = []
            self.num_vertices = 0

        def add_edge(self, src, dest, weight):
            self.graph.append([src, dest, weight])
            self.num_vertices += 1

        def find(self, parent, vertex):
            if parent[vertex] == vertex:
                return vertex
            
            return self.find(parent, parent[vertex])
                            
        def union(self, parent, rank, set1, set2):
            pass  
            

if __name__ == '__main__':
    sol = Solution()
    sol.main()
