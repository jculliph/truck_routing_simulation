# Given a list of vertices and edges, finds the shortest path between all vertices -> O(N^3)
def shortest_path(vertices, edges):

    distances = list(map(lambda i: list(map(lambda j: j, i)), edges))

    for k in range(vertices):
        for i in range(vertices):
            for j in range(vertices):
                distances[i][j] = min(distances[i][j], distances[i][k]+distances[k][j])

    return distances
