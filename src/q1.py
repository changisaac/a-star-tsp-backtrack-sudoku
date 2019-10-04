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

class TSPSolution:

    def __init__(self):
        self.data_dir = '../data/randTSP/'

    def main(self):
        f = open('q1_results_h0.txt', 'a')

        for i in range(1,17):
            print 'Number of Cities: ' + str(i)
            test_dir = self.data_dir + str(i) + '/'
            
            ave_num_nodes = 0
            num_passed = 0

            for j in range(1,11):
                print 'started test case # ' + str(j)
                test_file = test_dir +  'instance_' + str(j) + '.txt' 
                num_cities, g = self.read_in(test_file)
                
                start_time = time.time()
                final_path, dist_travelled, num_nodes, passed = self.a_star_tsp(num_cities, g, 'A')
                
                if passed:
                    ave_num_nodes += num_nodes
                    num_passed += 1

                    print 'final path: ' + str(final_path)
                    print 'distance travelled: ' + str(dist_travelled) + ' units'
                    print 'number of nodes generated: ' + str(num_nodes)
                    print 'time taken: ' + str(time.time() - start_time) + " second(s)" 
                else:
                    print 'FAILED'

                #self.display_cities(g, final_path)
            
            ave_num_nodes /= num_passed

            f.write(str(ave_num_nodes) + '\n')
            print "AVERAGE NUMBER OF NODES GENERATED: " + str(ave_num_nodes)


    def a_star_tsp(self, num_cities, g, s_city_name):
        s_time = time.time()

        num_nodes = 0
    
        s = g[s_city_name]

        q = PriorityQueue()

        q.put((0, [[s_city_name], 0]))
        num_nodes += 1
    
        while not q.empty():
            temp  = q.get()[1]
            path = temp[0]
            prev_acc_cost = temp[1]
        
            if time.time() - s_time > 300:
                return path, prev_acc_cost, num_nodes, False

            # Travelled all cities and then back to start
            if len(path) == num_cities + 1:
                return path, prev_acc_cost, num_nodes, True

            # Travelled all cities 
            if len(path) == num_cities:
                heur, acc_cost = self.calc_heur(g, path, s_city_name, s, prev_acc_cost)
                new_path = path[:]
                new_path.append(s_city_name)
                q.put((heur, [new_path, acc_cost]))
                num_nodes += 1
            # Haven't travelled all cities
            else:
                not_visited = set(path).symmetric_difference(set(g.keys()))

                for city in not_visited:
                    heur, acc_cost = self.calc_heur(g, path, city, s, prev_acc_cost)
                    new_path = path[:]
                    new_path.append(city)
                    q.put((heur, [new_path, acc_cost]))
                    num_nodes += 1

    # Heuristic Calculation Functions -----
    
    def calc_heur(self, g, path, next_city, s, prev_acc_cost):
        acc_cost = prev_acc_cost + self.eucl_dist(g[path[-1]], g[next_city])

        # Heuristic function 1
        #h1 = self.eucl_dist(g[next_city], s)

        # Heuristic function 2
        # h2 = self.calc_min_next_dist(g, path, next_city) 

        # Heuristic function 3
        #h3 = self.calc_mst_weight(g, path, next_city)

        # Zero Heuristic function
        #h0 = 0    

        f = acc_cost + 0

        return f, acc_cost

    def calc_mst_weight(self, g, path, next_city):
        new_path = path[:]
        new_path.append(next_city)

        not_visited = set(new_path).symmetric_difference(set(g.keys()))
        not_visited = list(not_visited)
        # for looping back to A start node
        not_visited.append('A')

        # find minimum spanning tree weight
        # generate edges
        edges = []

        for i in range(len(not_visited)):
            for j in range(len(not_visited)):
                if j != i:
                    src = not_visited[i]
                    dest = not_visited[j]
                    weight = self.eucl_dist(g[src], g[dest])
                    
                    edge = [src, dest, weight]
                    
                    edges.append(edge)

        mst_g = self.MST_Graph(not_visited)

        for src,dest,weight in edges:
            mst_g.add_edge(src, dest, weight)  

        return mst_g.get_mst_weight()

        pdb.set_trace()
    
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
        graph.plot(x_coords, y_coords)

        for i, label in enumerate(path):
            graph.annotate(label, (x_coords[i], y_coords[i]))

        plt.show()

    def test_mst(self):
        vertices = [0,1,2,3]
        g = self.MST_Graph(vertices)
        g.add_edge(0, 1, 10) 
        g.add_edge(0, 2, 6) 
        g.add_edge(0, 3, 5) 
        g.add_edge(1, 3, 15) 
        g.add_edge(2, 3, 4) 

        print g.get_mst_weight()

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
        
        def __init__(self, vertices):
            self.graph = []
            self.vertices = vertices

        def add_edge(self, src, dest, weight):
            self.graph.append([src, dest, weight])

        def find(self, parent, vertex):
            if parent[vertex] == vertex:
                return vertex
            
            return self.find(parent, parent[vertex])
                            
        def union(self, parent, rank, vertex_x, vertex_y):
            x_set = self.find(parent, vertex_x)
            y_set = self.find(parent, vertex_y)

            if rank[x_set] < rank[y_set]:
                parent[x_set] = y_set
            elif rank[x_set] > rank[y_set]:
                parent[y_set] = x_set
            else:
                # Just pick one
                parent[y_set] = x_set
                rank[x_set] += 1

        def get_mst_weight(self):
            # kruskal mst algorithm
            # sort graph by weight of edges
            self.graph = sorted(self.graph, key=lambda edge: edge[2])

            # initialize parent and rank arrays
            parent = {}
            rank = {}

            for vertex in self.vertices:
                parent[vertex] = vertex
                rank[vertex] = 0

            edge_count = 0
            mst_weight  = 0
            num_mst_edges = 0
    
            while num_mst_edges < len(self.vertices) - 1:
                src, dest, weight = self.graph[edge_count]
                
                edge_count += 1

                src_set = self.find(parent, src)
                dest_set = self.find(parent, dest)

                # if not in same set then add to mst weight
                if src_set != dest_set:
                    num_mst_edges += 1
                    mst_weight += weight
                    self.union(parent, rank, src, dest)

            return mst_weight

if __name__ == '__main__':
    sol = TSPSolution()
    sol.main()
