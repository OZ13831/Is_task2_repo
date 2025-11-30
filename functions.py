# ...existing code...
import os
import random
import networkx as nx
import matplotlib.pyplot as plt

def read_graph_from_txt(path):
    with open(path, 'r') as f:
        lines = [ln.strip() for ln in f if ln.strip()]

    start = int(lines[0])
    goal = int(lines[1])
    n = int(lines[2])
    edges = [[] for _ in range(n + 1)]

    for line in lines[3:]:
        u, v, w = map(int, line.split())
        edges[u].append((v, w))

    return n, start, goal, edges

def directed(n, p, wmin=1, wmax=30, allow_self=False, seed=None):
    if seed is not None:
        random.seed(seed)

    edges = []
    for u in range(1, n + 1):
        for v in range(1, n + 1):
            if not allow_self and u == v:
                continue
            if random.random() < p:
                w = random.randint(wmin, wmax)
                edges.append((u, v, w))
    return edges

def write_graph_txt(start, goal, n, edges, filename):
    graphs_dir = 'graphs'
    os.makedirs(graphs_dir, exist_ok=True)
    filepath = os.path.join(graphs_dir, filename)
    with open(filepath, "w") as f:
        f.write(f"{start}\n")
        f.write(f"{goal}\n")
        f.write(f"{n}\n")
        for u, v, w in edges:
            f.write(f"{u} {v} {w}\n")

def plot_graph(graph_name: str):
    num_nodes, start, goal, graph_edges = read_graph_from_txt(f'graphs/{graph_name}.txt')

    graph = nx.DiGraph()
    nnw = []
    # skip index 0 since nodes are 1-indexed in your format
    for node_id in range(1, len(graph_edges)):
        adj = graph_edges[node_id]
        if not adj:
            continue
        for (neighbour, weight) in adj:
            nnw.append((node_id, neighbour, weight))

    graph.add_weighted_edges_from(nnw)

    pos = nx.circular_layout(graph)
    plt.figure(figsize=(6,6))
    nx.draw_networkx_nodes(graph, pos, node_size=600)
    nx.draw_networkx_labels(graph, pos, font_size=12)
    nx.draw_networkx_edges(graph, pos, width=1.4, arrowstyle='-|>', arrowsize=10, connectionstyle='arc3,rad=0.0')

    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color='red')

    plt.axis('off')
    plt.show()
