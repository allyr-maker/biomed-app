# build_graph.py

import os
import re
import networkx as nx
from itertools import combinations
from pyvis.network import Network

def build_entity_graph(output_file="output.txt"):
    this_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(this_dir, output_file)

    if not os.path.exists(output_path):
        raise FileNotFoundError(f"{output_path} not found! Please generate it first.")

    # Step 1: Read and extract entities
    with open(output_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    chunks_entities = []
    current_entities = []

    for line in lines:
        line = line.strip()
        if line.startswith("--- ENTITIES"):
            current_entities = []
        elif line == "" or line.startswith("---") or line.startswith("SUMMARY"):
            if current_entities:
                chunks_entities.append(current_entities)
                current_entities = []
        elif "(" in line and ")" in line and "Confidence" in line:
            entity = line.split("(")[0].strip()
            current_entities.append(entity)

    # Step 2: Build the graph
    G = nx.Graph()
    for entity_list in chunks_entities:
        unique_entities = list(set(entity_list))
        for e1, e2 in combinations(unique_entities, 2):
            if G.has_edge(e1, e2):
                G[e1][e2]['weight'] += 1
            else:
                G.add_edge(e1, e2, weight=1)

    # Step 3: Create interactive visualization
    net = Network(height="750px", width="100%", notebook=False)
    net.from_nx(G)

    html_path = os.path.join(this_dir, "entity_graph.html")
    net.write_html(html_path)

    print(f"[✓] Graph successfully written to: {html_path}")
