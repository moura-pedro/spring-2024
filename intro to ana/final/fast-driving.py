"""
Filename: fast-driving.py
Author: Pedro Moura
Date: April 26, 2024
"""

import heapq

def dijkstra(n, graph):
    queue = [(-float('inf'), 1)]
    max_speed_to_node = {i: 0 for i in range(1, n + 1)}

    while queue:
        speed, node = heapq.heappop(queue)
        speed = -speed

        if node == n:
            return max_speed_to_node[node]

        for neighbor, path_speed in graph[node]:
            slowest_speed = min(speed, path_speed)
            
            if slowest_speed > max_speed_to_node[neighbor]:
                max_speed_to_node[neighbor] = slowest_speed
                heapq.heappush(queue, (-slowest_speed, neighbor))

    return 0



def get_edges():
    num_cities, num_roads = map(int, input().split())

    edges = []

    for i in range(num_roads):
        city1, city2, speed = map(int, input().split())
        edges.append((city1, city2, speed))
    
    return num_cities, edges



def gen_graph(n, edges):
    graph = {i: [] for i in range(1, n + 1)}

    for x, y, v in edges:
        graph[x].append((y, v))
        graph[y].append((x, v))

    return graph

def main():
    num_cities, edges = get_edges()
    graph = gen_graph(num_cities, edges)
    answer = dijkstra(num_cities, graph)

    print(answer)

main()
