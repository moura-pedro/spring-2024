"""
CSE4081 - Intro to Ana. Algo.
HW05 - "Joy" with Network Flows
Author - Pedro Moura
Date April 13, 2024

resources used: https://www.programiz.com/dsa/ford-fulkerson-algorithm
                Chap 26 T. Cormen's Intro to Algo (3rd Edition)
                Couple yt videos about Ford Fulkerson
"""

import sys

class Edge():
    def __init__(self, u, v, capacity):
        self.source = u
        self.sink = v
        self.capacity = capacity


class Graph():
    def __init__(self):
        self.adj_list = {}
        self.flow = {}



    def add_node(self, node):
        self.adj_list[node] = []



    def add_edge(self, u, v, capacity=0):
        if u != v:
            edge = Edge(u, v, capacity)
            backEdge = Edge(v, u, 0)

            edge.peer = backEdge
            backEdge.peer = edge

            self.adj_list[u].append(edge)
            self.adj_list[v].append(backEdge)

            self.flow[edge] = 0
            self.flow[backEdge] = 0



    def get_edges(self, node):
        return self.adj_list[node]



    def get_aug_path(self, s, t, path, set_path):
        if s == t:
            return path
        for edge in self.get_edges(s):
            leftover = edge.capacity - self.flow[edge]
            if leftover > 0 and (edge, leftover) not in set_path:
                set_path.add((edge, leftover))
                result = self.get_aug_path(edge.sink, t, path + [(edge, leftover)], set_path)
                if result != None:
                    return result



    def ford_fulkerson(self, s, t):
        aug_path = self.get_aug_path(s, t, [], set())

        while aug_path != None:
            flow = min(lftvr for edge, lftvr in aug_path)
            for edge, lftvr in aug_path:
                self.flow[edge] += flow
                self.flow[edge.peer] -= flow
            aug_path = self.get_aug_path(s, t, [], set())

        maxflow = sum(self.flow[edge] for edge in self.get_edges(s))
        return maxflow



    def load_nodes(self, not_eliminated, valid_matches):
        self.add_node("s")

        for match in valid_matches:
            self.add_node(match)

        for team in not_eliminated:
            self.add_node(team)
        
        self.add_node("t")



    def load_edges(self, valid_matches, teams_scores, not_eliminated):
        inf = 4000.0
        weight = 3

        curr_max = max(teams_scores.values())

        for edge in valid_matches:
            elem1, elem2 = edge
            self.add_edge('s', edge, weight)
            self.add_edge(edge, elem1, inf)
            self.add_edge(edge, elem2, inf)

        for team in not_eliminated:
            self.add_edge(team, 't', curr_max - not_eliminated[team])



    def load_graph(self, not_eliminated, valid_matches, teams_scores):
        self.load_nodes(not_eliminated, valid_matches)
        self.load_edges(valid_matches, teams_scores, not_eliminated)



def read_input(file_path):
    with open(file_path, 'r') as file:
        n = int(file.readline().strip())
        team_scores = {}
        
        for _ in range(n):
            team_name = file.readline().strip()
            score = int(file.readline().strip())
            team_scores[team_name] = score
            
        m = int(file.readline().strip())
        matches = []
        
        for _ in range(m):
            team1 = file.readline().strip()
            team2 = file.readline().strip()
            matches.append((team1, team2))
    
    return team_scores, matches



def check_elimination(team_scores, matches):
    remaining_games = {team: 0 for team in team_scores}
    for team1, team2 in matches:
        remaining_games[team1] += 1
        remaining_games[team2] += 1
    
    max_possible_points = {team: score + 3 * remaining_games[team] for team, score in team_scores.items()}

    current_highest_score = max(team_scores.values())

    eliminated = {}
    not_eliminated = {}
    for team, possible_points in max_possible_points.items():
        if possible_points < current_highest_score:
            eliminated[team] = (team_scores[team], "as it cannot catch up")
        else:
            not_eliminated[team] = (team_scores[team], possible_points)
    
    return eliminated, not_eliminated



def get_valid_matches(not_eliminated, matches):
    valid_matches = []
    for matche in matches:
        if matche[0] in not_eliminated and matche[1] in not_eliminated:
            valid_matches.append(matche)
    return valid_matches



def write_output(output, path):
    with open(path, 'w') as file:
        for line in output:
            file.write(line)



def main():
    team_scores, matches = read_input(sys.argv[1])

    output = ['Teams still challenging are...\n']
    sorted_scores = dict(sorted(team_scores.items(), key=lambda x:x[1], reverse=True))
    eliminated, not_eliminated = check_elimination(sorted_scores, matches)

    for team in sorted_scores:
        not_team = {t : sorted_scores[t] for t in sorted_scores if t != team}
        new_matches = [m for m in matches if team not in m]
        
        g = Graph()
        g.load_graph(not_team, new_matches, team_scores)
        if (team in not_eliminated):
            output.append('{} {} (flow = {})\n'.format(str(team), sorted_scores[team], g.ford_fulkerson('s', 't')))
    
    output.append("\nTeams that have been eliminated are...\n")

    for team in eliminated:
        output.append('{} {} ({})\n'.format(str(team), sorted_scores[team], eliminated[team][1]))

    write_output(output, sys.argv[2])

main()