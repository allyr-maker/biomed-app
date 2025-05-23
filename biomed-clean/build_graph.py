import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations

# Step 1: Read the saved output file
with open("output.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Step 2: Extract entity lines per chunk
chunks_entities = []
current_entities = []

for line in lines:
    line = line.strip()

    if line.startswith("--- ENTITIES"):
        current_entities = []  # start new entity list
    elif line == "" or line.startswith("---") or line.startswith("SUMMARY"):
        if current_entities:
            chunks_entities.append(current_entities)
            current_entities = []
    elif "(" in line and ")" in line and "Confidence" in line:
        # Extract the entity name
        entity = line.split("(")[0].strip()
        current_entities.append(entity)

# Step 3: Build graph
G = nx.Graph()

for entity_list in chunks_entities:
    unique_entities = list(set(entity_list))
    for entity1, entity2 in combinations(unique_entities, 2):
        if G.has_edge(entity1, entity2):
            G[entity1][entity2]['weight'] += 1
        else:
            G.add_edge(entity1, entity2, weight=1)

# Step 4: Draw the graph
plt.figure(figsize=(12, 10))
pos = nx.spring_layout(G, k=0.5)
nx.draw_networkx_nodes(G, pos, node_color='lightgreen', node_size=600)
nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.6)
nx.draw_networkx_labels(G, pos, font_size=9)
plt.title("Biomedical Entity Co-occurrence Graph")
plt.axis("off")
plt.tight_layout()
plt.show()
plt.savefig("entity_graph.png", dpi=300)

# interactive visualization
from pyvis.network import Network
import os

net = Network(notebook=False)
for node in G.nodes():
    net.add_node(node)
for u, v, d in G.edges(data=True):
    net.add_edge(u, v, value=d["weight"])

net.show("entity_graph.html")
# Optional: open the file manually if net.show doesn't launch browser
# os.system("start entity_graph.html")
