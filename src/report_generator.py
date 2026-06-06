import os


def generate_report(city_name, analysis, routes_data, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        file.write("RELATÓRIO DA MALHA URBANA\n")
        file.write("=" * 50 + "\n\n")

        file.write(f"Cidade/Bairro analisado: {city_name}\n\n")

        write_graph_summary(file, analysis)
        write_connected_nodes(file, analysis)
        write_connectivity(file, analysis)
        write_cycles(file, analysis)
        write_routes(file, routes_data)

    print(f"\nRelatório gerado: {output_path}")


def write_graph_summary(file, analysis):
    summary = analysis["summary"]

    file.write("1. RESUMO DO GRAFO\n")
    file.write("-" * 50 + "\n")
    file.write(f"Quantidade de nós: {summary['nodes']}\n")
    file.write(f"Quantidade de arestas: {summary['edges']}\n")
    file.write(f"Grafo direcionado: {summary['is_directed']}\n")
    file.write(f"Possui peso de distância: {summary['has_distance_weight']}\n")
    file.write(f"Possui peso de tempo: {summary['has_time_weight']}\n\n")


def write_connected_nodes(file, analysis):
    file.write("2. PONTOS MAIS CONECTADOS\n")
    file.write("-" * 50 + "\n")

    for index, item in enumerate(analysis["most_connected_nodes"], start=1):
        file.write(f"{index}. Nó {item['node']} - Conexões: {item['degree']}\n")

    file.write("\n")


def write_connectivity(file, analysis):
    file.write("3. CONECTIVIDADE\n")
    file.write("-" * 50 + "\n")
    file.write(f"Grafo conectado: {analysis['is_connected']}\n\n")


def write_cycles(file, analysis):
    file.write("4. CICLOS\n")
    file.write("-" * 50 + "\n")
    file.write(f"Possui ciclos: {analysis['has_cycle']}\n\n")


def write_routes(file, routes_data):
    file.write("5. ROTAS ANALISADAS\n")
    file.write("-" * 50 + "\n")

    file.write(f"Origem: {routes_data['origin']}\n")
    file.write(f"Destino: {routes_data['destination']}\n\n")

    write_route_result(file, "BFS Manual", routes_data["bfs"])
    write_route_result(file, "DFS Recursivo Manual", routes_data["dfs"])
    write_route_result(file, "Dijkstra Manual - Distância", routes_data["dijkstra_distance"])
    write_route_result(file, "Dijkstra Manual - Tempo", routes_data["dijkstra_time"])

    file.write("6. INTERPRETAÇÃO FINAL\n")
    file.write("-" * 50 + "\n")
    file.write(
        "A BFS encontrou um caminho considerando a menor quantidade de arestas, "
        "sem considerar diretamente a distância ou o tempo.\n"
    )
    file.write(
        "A DFS encontrou um caminho possível explorando o grafo em profundidade, "
        "mas não garante o menor custo.\n"
    )
    file.write(
        "O algoritmo de Dijkstra foi utilizado para encontrar a melhor rota ponderada, "
        "considerando distância ou tempo como peso das arestas.\n"
    )


def write_route_result(file, title, route_result):
    file.write(f"{title}\n")

    if route_result is None:
        file.write("Nenhuma rota encontrada.\n\n")
        return

    unit = "metros" if route_result["weight"] == "length" else "segundos"

    file.write(f"Algoritmo: {route_result['algorithm']}\n")
    file.write(f"Quantidade de pontos: {route_result['total_nodes']}\n")
    file.write(f"Peso usado: {route_result['weight']}\n")
    file.write(f"Custo total: {route_result['total_cost']:.2f} {unit}\n")
    file.write("Caminho:\n")
    file.write(" -> ".join(str(node) for node in route_result["path"]))
    file.write("\n\n")