import os
import osmnx as ox


def load_graph(city_name: str, cache_path: str):
    if os.path.exists(cache_path):
        print("Carregando grafo do cache local...")
        return ox.io.load_graphml(cache_path)

    print("Baixando grafo do OpenStreetMap...")

    graph = ox.graph_from_place(
        city_name,
        network_type="drive",
        simplify=True,
        retain_all=False
    )

    graph = ox.routing.add_edge_speeds(graph, fallback=30)
    graph = ox.routing.add_edge_travel_times(graph)

    ox.io.save_graphml(graph, cache_path)

    return graph