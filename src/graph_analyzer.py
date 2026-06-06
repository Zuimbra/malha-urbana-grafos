# ==========================================================
# RESUMO DO GRAFO
# ==========================================================

def get_graph_summary(graph):
    return {
        "nodes": graph.number_of_nodes(),
        "edges": graph.number_of_edges(),
        "is_directed": graph.is_directed(),
        "has_distance_weight": has_edge_attribute(graph, "length"),
        "has_time_weight": has_edge_attribute(graph, "travel_time")
    }


def has_edge_attribute(graph, attribute_name):
    for _, _, data in graph.edges(data=True):
        if attribute_name in data:
            return True

    return False


def print_graph_summary(summary):
    print("\nResumo do grafo:")
    print(f"Nós: {summary['nodes']}")
    print(f"Arestas: {summary['edges']}")
    print(f"Direcionado: {summary['is_directed']}")
    print(f"Possui peso de distância: {summary['has_distance_weight']}")
    print(f"Possui peso de tempo: {summary['has_time_weight']}")


# ==========================================================
# VIZINHOS
# ==========================================================

def get_neighbors(graph, node):
    """
    Retorna os vizinhos do nó.

    Se o grafo for direcionado, considera tanto:
    - ruas que saem do nó
    - ruas que chegam no nó

    Isso ajuda a analisar a conectividade geral da região.
    """
    neighbors = set()

    if graph.is_directed():
        for neighbor in graph.successors(node):
            neighbors.add(neighbor)

        for neighbor in graph.predecessors(node):
            neighbors.add(neighbor)
    else:
        for neighbor in graph.neighbors(node):
            neighbors.add(neighbor)

    return list(neighbors)


def get_successors(graph, node):
    """
    Retorna apenas os vizinhos alcançáveis respeitando a direção da aresta.
    """
    if graph.is_directed():
        return list(graph.successors(node))

    return list(graph.neighbors(node))


# ==========================================================
# PONTOS MAIS CONECTADOS
# ==========================================================

def get_most_connected_nodes(graph, limit=10):
    connected_nodes = []

    for node in graph.nodes:
        degree = len(get_neighbors(graph, node))

        connected_nodes.append({
            "node": node,
            "degree": degree
        })

    connected_nodes.sort(key=lambda item: item["degree"], reverse=True)

    return connected_nodes[:limit]


def print_most_connected_nodes(nodes):
    print("\nPontos mais conectados:")

    for index, item in enumerate(nodes, start=1):
        print(f"{index}. Nó {item['node']} - Conexões: {item['degree']}")


# ==========================================================
# CONECTIVIDADE COM DFS
# ==========================================================

def dfs_visit(graph, current_node, visited):
    visited.add(current_node)

    for neighbor in get_neighbors(graph, current_node):
        if neighbor not in visited:
            dfs_visit(graph, neighbor, visited)


def is_connected_with_dfs(graph):
    """
    Verifica se o grafo é conectado usando DFS.

    Aqui a direção das ruas é ignorada para analisar se a região urbana
    está ligada como uma malha.
    """
    nodes = list(graph.nodes)

    if len(nodes) == 0:
        return False

    visited = set()
    start_node = nodes[0]

    dfs_visit(graph, start_node, visited)

    return len(visited) == graph.number_of_nodes()


# ==========================================================
# CICLOS COM DFS
# ==========================================================

def has_cycle_with_dfs(graph):
    """
    Detecta ciclo usando DFS.

    Para grafo direcionado, usa pilha de recursão.
    """
    visited = set()
    recursion_stack = set()

    def dfs(current_node):
        visited.add(current_node)
        recursion_stack.add(current_node)

        for neighbor in get_successors(graph, current_node):
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
            elif neighbor in recursion_stack:
                return True

        recursion_stack.remove(current_node)
        return False

    for node in graph.nodes:
        if node not in visited:
            if dfs(node):
                return True

    return False


# ==========================================================
# ANÁLISE GERAL
# ==========================================================

def analyze_graph(graph):
    return {
        "summary": get_graph_summary(graph),
        "most_connected_nodes": get_most_connected_nodes(graph, limit=10),
        "is_connected": is_connected_with_dfs(graph),
        "has_cycle": has_cycle_with_dfs(graph)
    }


def print_graph_analysis(analysis):
    print_graph_summary(analysis["summary"])

    print_most_connected_nodes(analysis["most_connected_nodes"])

    print("\nConectividade:")
    print(f"Grafo conectado: {analysis['is_connected']}")

    print("\nCiclos:")
    print(f"Possui ciclos: {analysis['has_cycle']}")