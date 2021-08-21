import graph as gr
import cli

print()
graph = gr.Graph(cli.args.file)
action_done = False

if cli.args.info:
    print(f"Graph from {cli.args.file}:\n")
    graph.print_graph_info()
    action_done = True

if cli.args.bfs is not None:
    print(f"Breadth-first search in vertex {cli.args.bfs}:\n")
    graph.breadth_first_search(cli.args.bfs)
    action_done = True

if cli.args.euler_cycle:
    print(f"Euler cycle:\n")
    graph.euler_cycle()
    action_done = True

if cli.args.bellman_ford is not None:
    print(f"Bellman-Ford algorithm in vertex {cli.args.bellman_ford}:\n")
    graph.bellman_ford(cli.args.bellman_ford)
    action_done = True

if cli.args.dijkstra is not None:
    print(f"Dijkstra algorithm in vertex {cli.args.dijkstra}:\n")
    graph.dijkstra(cli.args.dijkstra)
    action_done = True

if cli.args.floyd_warshall:
    print(f"Floyd-Warshall algorithm:\n")
    graph.floyd_warshall()
    action_done = True

if cli.args.strongly_connected:
    print(f"Strongly connected components:\n")
    graph.strongly_connected_components()
    action_done = True

if cli.args.topological_ordering:
    print(f"Topological order:\n")
    graph.topological_ordering()
    action_done = True

if cli.args.kruskal:
    print(f"Kruskal's minimum spanning tree:\n")
    graph.kruskal()
    action_done = True

if cli.args.prim:
    print(f"Prim's minimum spanning tree:\n")
    graph.prim()
    action_done = True

if not action_done:
    print("Welp, nothing to be done. Maybe you want to check -h and add some flags next time.")
