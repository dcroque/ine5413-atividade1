import argparse
from typing import Union

def fix_type(arg: str) -> Union[str, int]:
    try:
        return int(arg)
    except:
        return arg

parser = argparse.ArgumentParser(description='Read graph from file and apply some actions to them')
parser.add_argument('-file',
                    type=str,
                    required=True,
                    help='Path for graph file')

parser.add_argument('-i',
                    '--info',
                    action='store_true',
                    help='Output info about vertex and edges from the given file')

parser.add_argument('-s',
                    '--bfs',
                    type= str,
                    action='store',
                    help='Output the result of a Breadth-first search based on the label or index provided')

parser.add_argument('-e',
                    '--euler_cycle',
                    action='store_true',
                    help='Output if the graph has an Euler cycle and the cycle itself')

parser.add_argument('-bf',
                    '--bellman_ford',
                    type= str,
                    action='store',
                    help='Output the result of a Bellman-Ford algorithm based on the label or index provided')

parser.add_argument('-d',
                    '--dijkstra',
                    type= str,
                    action='store',
                    help='Output the result of a Dijkstra algorithm based on the label or index provided')   

parser.add_argument('-fw',
                    '--floyd_warshall',
                    action='store_true',
                    help='Output the result of a Floyd-Warshall algorithm based on the label or index provided')

parser.add_argument('-scc',
                    '--strongly_connected',
                    action='store_true',
                    help='Output all the strongly connected components of the graph')

parser.add_argument('-to',
                    '--topological_ordering',
                    action='store_true',
                    help='Output a valid topological ordering for the graph')

parser.add_argument('-k',
                    '--kruskal',
                    action='store_true',
                    help='Output the minimum spanning tree using the Kruskal algorithm')

parser.add_argument('-p',
                    '--prim',
                    action='store_true',
                    help='Output the minimum spanning tree using the Prim algorithm')              

args = parser.parse_args()

if args.bfs is not None:
    args.bfs = fix_type(args.bfs)

if args.euler_cycle is not None:
    args.euler_cycle = fix_type(args.euler_cycle)

if args.dijkstra is not None:
    args.dijkstra = fix_type(args.dijkstra)

if args.floyd_warshall is not None:
    args.floyd_warshall = fix_type(args.floyd_warshall)