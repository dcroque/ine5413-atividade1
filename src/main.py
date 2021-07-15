import graph as gr
import cli

# test_data
#
# 2   5   8
#  \  |
#   1-4---7
#  /   \ /
# 3     6   

graph = gr.Graph(cli.args.file)

if cli.args.bfs is not None:
    print(f"Breadth-first search in vertex {cli.args.bfs}:\n")
    graph.bellman_ford(cli.args.bfs)

if cli.args.euler_cycle:
    print(f"Euler cycle:\n")
    graph.bellman_ford(cli.args.euler_cycle)

if cli.args.bellman_ford is not None:
    print(f"Bellman-Ford algorithm in vertex {cli.args.bellman_ford}:\n")
    graph.bellman_ford(cli.args.bellman_ford)

if cli.args.dijkstra is not None:
    print(f"Dijkstra algorithm in vertex {cli.args.dijkstra}:\n")
    graph.bellman_ford(cli.args.dijkstra)

if cli.args.floyd_warshall is not None:
    print(f"Floyd-Warshall algorithm in vertex {cli.args.floyd_warshall}:\n")
    graph.bellman_ford(cli.args.floyd_warshall)
