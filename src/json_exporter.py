import json
import os


def save_json(data, output_path):
    """
    Salva qualquer dicionário/lista em formato JSON.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(
            convert_to_json_compatible(data),
            file,
            ensure_ascii=False,
            indent=4
        )

    print(f"\nArquivo JSON gerado: {output_path}")


def export_graph_to_json(graph, output_path):
    """
    Exporta a malha urbana do grafo para JSON.
    """
    graph_data = {
        "metadata": {
            "total_vertices": graph.number_of_nodes(),
            "total_edges": graph.number_of_edges(),
            "is_directed": graph.is_directed()
        },
        "vertices": [],
        "arestas": []
    }

    for node_id, attributes in graph.nodes(data=True):
        graph_data["vertices"].append({
            "id": str(node_id),
            "latitude": attributes.get("y"),
            "longitude": attributes.get("x")
        })

    for origin, destination, key, attributes in graph.edges(keys=True, data=True):
        graph_data["arestas"].append({
            "id": f"{origin}-{destination}-{key}",
            "origem": str(origin),
            "destino": str(destination),
            "distancia_metros": attributes.get("length"),
            "tempo_segundos": attributes.get("travel_time"),
            "velocidade_kmh": attributes.get("speed_kph"),
            "nome_rua": normalize_value(attributes.get("name")),
            "tipo_via": normalize_value(attributes.get("highway"))
        })

    save_json(graph_data, output_path)


def export_routes_to_json(routes_data, output_path):
    """
    Exporta os resultados das rotas para JSON.
    """
    save_json(routes_data, output_path)


def export_analysis_to_json(analysis_data, output_path):
    """
    Exporta a análise geral do grafo para JSON.
    """
    save_json(analysis_data, output_path)


def normalize_value(value):
    """
    Normaliza valores vindos do OSMnx.
    """
    if value is None:
        return None

    if isinstance(value, (str, int, float, bool)):
        return value

    if isinstance(value, (list, tuple, set)):
        return [normalize_value(item) for item in value]

    return str(value)


def convert_to_json_compatible(value):
    """
    Converte valores que podem dar problema ao salvar em JSON.
    """
    if value is None:
        return None

    if isinstance(value, (str, int, float, bool)):
        return value

    if isinstance(value, dict):
        return {
            str(key): convert_to_json_compatible(item)
            for key, item in value.items()
        }

    if isinstance(value, (list, tuple, set)):
        return [
            convert_to_json_compatible(item)
            for item in value
        ]

    return str(value)