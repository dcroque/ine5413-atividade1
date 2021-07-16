import graph as gr
import cli

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

if cli.args.floyd_warshall is not None:
    print(f"Floyd-Warshall algorithm in vertex {cli.args.floyd_warshall}:\n")
    graph.floyd_Warshall(cli.args.floyd_warshall)
    action_done = True

if not action_done:
    print("Welp, nothing to be done. Maybe you want to check -h and add some flags next time.")
