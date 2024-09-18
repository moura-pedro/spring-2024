def parse_input(file_path):
    with open(file_path, 'r') as file:
        n = int(file.readline().strip())
        teams = {}
        
        for _ in range(n):
            team_name = file.readline().strip()
            score = int(file.readline().strip())
            teams[team_name] = {'score': score, 'games': []}
        
        m = int(file.readline().strip())
        
        for _ in range(m):
            x = file.readline().strip()
            y = file.readline().strip()
            teams[x]['games'].append(y)
            teams[y]['games'].append(x)
    
    return teams


def build_graph(teams, excluded_team):
    graph = {'source': {}, 'sink': {}}
    total_matches = 0
    
    # Initialize match nodes and team connections
    for team, data in teams.items():
        if team == excluded_team:
            continue
        for opponent in data['games']:
            if opponent == excluded_team or (opponent, team) in graph or (team, opponent) in graph:
                continue
            match_node = f"match_{team}_{opponent}"
            graph['source'][match_node] = 3  # Edge from source to match node
            graph[match_node] = {team: float('inf'), opponent: float('inf')}
            total_matches += 3
    
    # Add edges from teams to sink
    excluded_points = teams[excluded_team]['score'] + 3 * len(teams[excluded_team]['games'])
    for team in teams:
        if team == excluded_team:
            continue
        max_points = teams[team]['score'] + 3 * len(teams[team]['games'])
        graph[team] = {'sink': max(max_points - excluded_points, 0)}

    return graph, total_matches


def dfs_find_path(graph, current, sink, path, visited):
    if current == sink:
        return path
    visited.add(current)
    for neighbor in graph[current]:
        if neighbor not in visited and graph[current][neighbor] > 0:  # Check for residual capacity
            result = dfs_find_path(graph, neighbor, sink, path + [(current, neighbor)], visited)
            if result is not None:
                return result
    return None

def ford_fulkerson(graph, source, sink):
    max_flow = 0
    visited = set()
    path = dfs_find_path(graph, source, sink, [], visited)
    
    while path:
        # Find the minimum capacity in the path
        flow = min(graph[u][v] for u, v in path)
        
        # Update the capacities in the graph for the forward and reverse edges
        for u, v in path:
            graph[u][v] -= flow
            graph[v][u] = graph.get(v, {}).get(u, 0) + flow
        
        max_flow += flow
        visited = set()
        path = dfs_find_path(graph, source, sink, [], visited)
    
    return max_flow



def determine_elimination(teams):
    results = {}
    for team in teams:
        graph, total_matches = build_graph(teams, team)
        flow_value = ford_fulkerson(graph, 'source', 'sink')
        if flow_value >= total_matches:
            results[team] = ('not eliminated', flow_value)
        else:
            results[team] = ('eliminated', flow_value)
    return results


def output_results(results, output_file):
    with open(output_file, 'w') as file:
        file.write("Teams still challenging are...\n")
        for team, (status, flow) in results.items():
            if status == 'not eliminated':
                file.write(f"{team} (flow = {flow})\n")
        file.write("\nTeams that have been eliminated are...\n")
        for team, (status, flow) in results.items():
            if status == 'eliminated':
                file.write(f"{team} (flow = {flow})\n")


def main ():

    teams = parse_input("matches300.in")
    results = determine_elimination(teams)
    output_results(results, "xablau.out")

main()
