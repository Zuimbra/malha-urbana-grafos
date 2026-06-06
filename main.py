import sys

from src.config import (
    CITY_NAME,
    RAW_GRAPH_PATH,
    PROCESSED_GRAPH_JSON_PATH,
    ROUTES_OUTPUT_PATH,
    ANALYSIS_OUTPUT_PATH,
    REPORT_OUTPUT_PATH
)

from src.graph_loader import load_graph
from src.graph_analyzer import analyze_graph, print_graph_analysis

from src.json_exporter import (
    export_graph_to_json,
    export_routes_to_json,
    export_analysis_to_json
)

from src.report_generator import generate_report

from src.route_service import (
    bfs_find_path,
    bfs_path_exists,
    dfs_find_path_recursive,
    dfs_path_exists_recursive,
    dijkstra_shortest_path,
    create_route_result,
    print_route_result
)


sys.setrecursionlimit(10000)


def main():
    graph = load_graph(CITY_NAME, RAW_GRAPH_PATH)

    print(f"\nGrafo carregado com {graph.number_of_nodes()} nós e {graph.number_of_edges()} arestas.")
    print(f"Cidade/Bairro: {CITY_NAME}")

    print("\n==============================")
    print("ANÁLISE GERAL DO GRAFO")
    print("==============================")

    analysis = analyze_graph(graph)
    print_graph_analysis(analysis)

    print("\n==============================")
    print("EXPORTANDO GRAFO PARA JSON")
    print("==============================")

    export_graph_to_json(graph, PROCESSED_GRAPH_JSON_PATH)

    nodes = list(graph.nodes)

    origin = nodes[0]
    destination = nodes[89]

    print(f"\nOrigem escolhida: {origin}")
    print(f"Destino escolhido: {destination}")

    print("\n==============================")
    print("BFS MANUAL")
    print("==============================")

    bfs_exists = bfs_path_exists(graph, origin, destination)
    print(f"Existe caminho com BFS? {bfs_exists}")

    bfs_path = bfs_find_path(graph, origin, destination)

    bfs_result = create_route_result(
        graph=graph,
        origin=origin,
        destination=destination,
        path=bfs_path,
        algorithm="BFS Manual",
        weight="length"
    )

    print_route_result(bfs_result)

    print("\n==============================")
    print("DFS RECURSIVO MANUAL")
    print("==============================")

    dfs_exists = dfs_path_exists_recursive(graph, origin, destination)
    print(f"Existe caminho com DFS? {dfs_exists}")

    dfs_path = dfs_find_path_recursive(graph, origin, destination)

    dfs_result = create_route_result(
        graph=graph,
        origin=origin,
        destination=destination,
        path=dfs_path,
        algorithm="DFS Recursivo Manual",
        weight="length"
    )

    print_route_result(dfs_result)

    print("\n==============================")
    print("DIJKSTRA MANUAL - DISTÂNCIA")
    print("==============================")

    dijkstra_distance_result = dijkstra_shortest_path(
        graph=graph,
        origin=origin,
        destination=destination,
        weight="length"
    )

    print_route_result(dijkstra_distance_result)

    print("\n==============================")
    print("DIJKSTRA MANUAL - TEMPO")
    print("==============================")

    dijkstra_time_result = dijkstra_shortest_path(
        graph=graph,
        origin=origin,
        destination=destination,
        weight="travel_time"
    )

    print_route_result(dijkstra_time_result)

    print("\n==============================")
    print("EXPORTANDO RESULTADOS")
    print("==============================")

    routes_data = {
        "origin": origin,
        "destination": destination,
        "bfs": bfs_result,
        "dfs": dfs_result,
        "dijkstra_distance": dijkstra_distance_result,
        "dijkstra_time": dijkstra_time_result
    }

    export_routes_to_json(routes_data, ROUTES_OUTPUT_PATH)
    export_analysis_to_json(analysis, ANALYSIS_OUTPUT_PATH)

    print("\n==============================")
    print("GERANDO RELATÓRIO")
    print("==============================")

    generate_report(
        city_name=CITY_NAME,
        analysis=analysis,
        routes_data=routes_data,
        output_path=REPORT_OUTPUT_PATH
    )

    print("\nProcesso finalizado com sucesso.")


if __name__ == "__main__":
    main()