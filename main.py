from flask import Flask, render_template, request
import networkx as nx
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    image_path_original = None
    image_path_solution = None
    nodes = edges = origen = destino = ""

    if request.method == "POST":
        action = request.form["action"]

        # 🧹 Si se presiona "Nuevo"
        if action == "nuevo":
            for filename in ["original.png", "solution.png"]:
                path = os.path.join("static", filename)
                if os.path.exists(path):
                    os.remove(path)
            return render_template("index.html")

        # ✅ Si se presiona "Calcular"
        nodes = request.form["nodes"]
        edges = request.form["edges"]
        origen = request.form["origen"]
        destino = request.form["destino"]

        G = nx.Graph()

        for node in nodes.split(","):
            G.add_node(node.strip())

        for edge in edges.split(";"):
            u, v, w = edge.strip().split(",")
            G.add_edge(u.strip(), v.strip(), weight=float(w))

        pos = nx.spring_layout(G)

        # Grafo original
        plt.figure(figsize=(6, 5))
        nx.draw(G, pos, with_labels=True, node_color='lightgray', node_size=700, font_size=12)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        original_path = os.path.join("static", "original.png")
        plt.savefig(original_path)
        plt.close()

        try:
            shortest_path = nx.dijkstra_path(G, origen, destino)
            path_edges = list(zip(shortest_path, shortest_path[1:]))

            # Grafo resaltado
            plt.figure(figsize=(6, 5))
            nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=700, font_size=12)
            nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='gray', width=1)
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3)
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
            solution_path = os.path.join("static", "solution.png")
            plt.savefig(solution_path)
            plt.close()

            result = "Ruta más corta: " + " → ".join(shortest_path)
            image_path_original = original_path
            image_path_solution = solution_path

        except Exception as e:
            result = f"Error al calcular la ruta: {e}"

    return render_template("index.html", result=result,
                           image_path_original=image_path_original,
                           image_path_solution=image_path_solution,
                           nodes=nodes, edges=edges,
                           origen=origen, destino=destino)

if __name__ == "__main__":
    app.run(debug=True)
