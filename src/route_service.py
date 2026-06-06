from collections import deque
import heapq


# ==========================================================
# FUNÇÕES DE VIZINHANÇA
# ==========================================================

def get_neighbor_nodes(graph, node):
    """
    Retorna os vizinhos de um nó.

    Em grafos direcionados, usa successors().
    Em grafos não direcionados, usa neighbors().
    """
    if graph.is_directed():
        return list(graph.successors(node))

    return list(graph.neighbors(node))


def get_best_edge_weight(graph, origin, destination, weight="length"):
    """
    Retorna o menor peso entre duas arestas.

    No grafo do OSMnx, pode existir mais de uma aresta entre dois mesmos nós.
    Por isso, pegamos a menor aresta disponível para o peso escolhido.
    """
    edges = graph.get_edge_data(origin, destination)

    if edges is None:
        return float("inf")

    # Caso seja um grafo simples, edge_data pode ser o próprio dicionário da aresta.
    if weight in edges:
        return float(edges.get(weight, float("inf")))

    # Caso seja MultiDiGraph/MultiGraph, edges é um dicionário de arestas.
    best_weight = float("inf")

    for edge_data in edges.values():
        if isinstance(edge_data, dict):
            edge_weight = edge_data.get(weight, float("inf"))

            if edge_weight is not None:
                edge_weight = float(edge_weight)

                if edge_weight < best_weight:
                    best_weight = edge_weight

    return best_weight


def get_weighted_neighbors(graph, node, weight="length"):
    """
    Retorna os vizinhos de um nó junto com o peso da conexão.

    Exemplo:
    [
        (vizinho_1, 120.5),
        (vizinho_2, 80.0)
    ]
    """
    weighted_neighbors = []

    for neighbor in get_neighbor_nodes(graph, node):
        edge_weight = get_best_edge_weight(graph, node, neighbor, weight)

        if edge_weight != float("inf"):
            weighted_neighbors.append((neighbor, edge_weight))

    return weighted_neighbors


# ==========================================================
# BFS MANUAL
# ==========================================================

def bfs_find_path(graph, origin, destination):
    """
    Encontra um caminho entre origem e destino usando BFS.

    A BFS encontra o caminho com menor quantidade de arestas,
    mas não necessariamente o menor caminho por distância ou tempo.
    """
    if origin not in graph.nodes or destination not in graph.nodes:
        return None

    queue = deque()
    visited = set()
    previous = {}

    queue.append(origin)
    visited.add(origin)
    previous[origin] = None

    while queue:
        current = queue.popleft()

        if current == destination:
            return build_path(previous, destination)

        for neighbor in get_neighbor_nodes(graph, current):
            if neighbor not in visited:
                visited.add(neighbor)
                previous[neighbor] = current
                queue.append(neighbor)

    return None


def bfs_path_exists(graph, origin, destination):
    """
    Verifica se existe caminho entre origem e destino usando BFS.
    """
    return bfs_find_path(graph, origin, destination) is not None


# ==========================================================
# DFS RECURSIVO MANUAL
# ==========================================================

def dfs_find_path_recursive(graph, origin, destination):
    """
    Encontra um caminho entre origem e destino usando DFS recursivo.

    A DFS encontra um caminho possível, mas não garante:
    - menor quantidade de arestas;
    - menor distância;
    - menor tempo.
    """
    if origin not in graph.nodes or destination not in graph.nodes:
        return None

    visited = set()
    path = []

    def dfs(current):
        visited.add(current)
        path.append(current)

        if current == destination:
            return True

        for neighbor in get_neighbor_nodes(graph, current):
            if neighbor not in visited:
                if dfs(neighbor):
                    return True

        path.pop()
        return False

    if dfs(origin):
        return path

    return None


def dfs_path_exists_recursive(graph, origin, destination):
    """
    Verifica se existe caminho entre origem e destino usando DFS recursivo.
    """
    return dfs_find_path_recursive(graph, origin, destination) is not None


# ==========================================================
# DIJKSTRA MANUAL
# ==========================================================

def dijkstra_shortest_path(graph, origin, destination, weight="length"):
    """
    Calcula a menor rota entre origem e destino usando Dijkstra manual.

    Use:
    weight="length"      para menor distância
    weight="travel_time" para menor tempo
    """
    if origin not in graph.nodes or destination not in graph.nodes:
        return None

    distances = {}
    previous = {}
    visited = set()

    for node in graph.nodes:
        distances[node] = float("inf")

    distances[origin] = 0
    previous[origin] = None

    priority_queue = []
    heapq.heappush(priority_queue, (0, origin))

    while priority_queue:
        current_distance, current = heapq.heappop(priority_queue)

        if current in visited:
            continue

        visited.add(current)

        if current == destination:
            break

        for neighbor, edge_weight in get_weighted_neighbors(graph, current, weight):
            new_distance = current_distance + edge_weight

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current
                heapq.heappush(priority_queue, (new_distance, neighbor))

    if distances[destination] == float("inf"):
        return None

    path = build_path(previous, destination)

    return {
        "algorithm": "Dijkstra Manual",
        "origin": origin,
        "destination": destination,
        "path": path,
        "total_cost": distances[destination],
        "weight": weight,
        "total_nodes": len(path)
    }


# ==========================================================
# FUNÇÕES AUXILIARES
# ==========================================================

def build_path(previous, destination):
    """
    Reconstrói o caminho final usando o dicionário de predecessores.

    Exemplo:
    previous = {
        B: A,
        C: B,
        D: C
    }

    Resultado:
    A -> B -> C -> D
    """
    path = []
    current = destination

    while current is not None:
        path.append(current)
        current = previous.get(current)

    path.reverse()

    return path


def calculate_route_cost(graph, path, weight="length"):
    """
    Calcula o custo total de uma rota.

    Exemplo:
    A -> B -> C

    custo total =
    custo(A, B) + custo(B, C)
    """
    if path is None or len(path) < 2:
        return 0

    total_cost = 0

    for current, next_node in zip(path[:-1], path[1:]):
        edge_weight = get_best_edge_weight(graph, current, next_node, weight)

        if edge_weight != float("inf"):
            total_cost += edge_weight

    return total_cost


def create_route_result(graph, origin, destination, path, algorithm, weight="length"):
    """
    Cria um resultado padronizado para BFS ou DFS.

    Dijkstra já retorna o resultado completo sozinho.
    """
    if path is None:
        return None

    return {
        "algorithm": algorithm,
        "origin": origin,
        "destination": destination,
        "path": path,
        "total_cost": calculate_route_cost(graph, path, weight),
        "weight": weight,
        "total_nodes": len(path)
    }


def print_route_result(route_result):
    """
    Imprime o resultado da rota no terminal, sempre mostrando o caminho completo.
    """
    if route_result is None:
        print("\nNenhuma rota encontrada.")
        return

    unit = "metros" if route_result["weight"] == "length" else "segundos"

    print("\nRota encontrada:")
    print(f"Algoritmo: {route_result['algorithm']}")
    print(f"Origem: {route_result['origin']}")
    print(f"Destino: {route_result['destination']}")
    print(f"Peso usado: {route_result['weight']}")
    print(f"Quantidade de pontos: {route_result['total_nodes']}")
    print(f"Custo total: {route_result['total_cost']:.2f} {unit}")

    print("Caminho completo:")
    print(" -> ".join(str(node) for node in route_result["path"]))


def print_path(path):
    """
    Imprime somente o caminho.
    """
    if path is None:
        print("Nenhum caminho encontrado.")
        return

    print("Caminho:")
    print(" -> ".join(str(node) for node in path))