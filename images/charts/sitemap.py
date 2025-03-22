import matplotlib.pyplot as plt
import networkx as nx

# Create the directed graph
G = nx.DiGraph()

# Updated nodes
nodes = {
    "start": "Clinician Accesses CDSS",
    "form_submission": "Fills Out Form\n & Submits Data",
    "predict_route": "Backend (/predict)\nValidates Input\n & Aligns Features",
    "model": "Logistic Regression Model\nMakes Prediction",
    "db_save": "Saves Data to Database",
    "result_page": "Redirects to Patient Page\n & Displays Patient Profile and Prediction",
    "output": "Output:\nPrediction (Resistant/Not Resistant)"
}

# Add edges
edges = [
    ("start", "form_submission"),
    ("form_submission", "predict_route"),
    ("predict_route", "model"),
    ("model", "db_save"),
    ("db_save", "result_page"),
    ("result_page", "output")
]

# Add nodes and edges to graph
G.add_nodes_from(nodes.keys())
G.add_edges_from(edges)

# Define positions for nodes
pos = {
    "start": (0, 5),
    "form_submission": (0, 4),
    "predict_route": (0, 3),
    "model": (-1, 2),
    "db_save": (1, 2),
    "result_page": (0, 1),
    "output": (0, 0)
}

# Create the plot
plt.figure(figsize=(10, 8))
nx.draw_networkx_edges(G, pos, arrowstyle="->", arrowsize=15, edge_color="black")
nx.draw_networkx_nodes(G, pos, node_size=4000, node_color="lightblue", node_shape="o", linewidths=1)
nx.draw_networkx_labels(G, pos, labels=nodes, font_size=10, font_color="black")

# Title
plt.title("Sitemap Flow Diagram: Clinician Workflow while using CDSS Predictor Model", fontsize=14)
plt.axis("off")
plt.show()
