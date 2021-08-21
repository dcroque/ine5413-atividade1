from os import error, getrandom, truncate
from typing import Union, Tuple
import heapq

class Graph:
    def __init__(self, file: str) -> None:
        self.__vertices: "list['Vertex']" = []
        self.__edges: "list['Edge']" = []
        self.__load_file(file)
        self.__directed = False


    def __load_file(self, file: str) -> None:
        """Busca dados e insere os dados de um arquivo no grafo."""
        try:
            data = open(file, 'r')
            lines = data.readlines()

            for line in lines:
                sp_line = line.split()
                sp_types = [self.__input_type(a) for a in sp_line]
                    
                if sp_line[0][0] == "#" or sp_line[0][0] == "*":
                    if sp_line[0] == "*edges":
                        self.__directed = False
                    if sp_line[0] == "*arcs":
                        self.__directed = True                 
                else:
                    if sp_types[0] != sp_types[1]:
                        self.__vertices.append(Vertex(int(sp_line[0]), sp_line[1]))
                    else:
                        w = 1
                        if len(sp_types) > 2:
                            w = float(sp_line[2])
                        if sp_types[0] == "int":
                            self.__edges.append(Edge(int(sp_line[0]), int(sp_line[1]), float(sp_line[2])))
                        else:
                            vertex1 = self.vertex_index(sp_line[0])
                            vertex2 = self.vertex_index(sp_line[1])
                            self.__edges.append(Edge(vertex1, vertex2, float(sp_line[2])))
        except Exception as err:
            print(f"{err}\nSomething went wrong while loading the requested file.\nPlease, check the README file for more information about the input files")
            exit()

    def __input_type(self, value: Union[str, int]) -> str:
        try:
            a = int(value)
            return "int"
        except ValueError:
            return "str"

    def print_graph_info(self):
        for ele in self.__vertices:
            print(f'n{ele.get_idx()}: {ele.get_label()}')
        print("\nARESTAS\n")
        for ele in self.__edges:
            print(f'{ele.get_origin()} -> {ele.get_destiny()}: peso {ele.get_weight()}')
        print()

    def find_vertex(self, arg: Union[str, int]) -> 'Vertex':
        """Retorna o Vertex especificado por rotulo ou indice."""
        return self.__vertex_by_idx(arg) if isinstance(arg, int) else self.__vertex_by_label(arg)

    def __vertex_by_idx(self, idx: int) -> 'Vertex':
        """Retorna o Vertex especificado por indice."""
        return self.__vertices[idx-1] if idx > 0 and idx <= len(self.__vertices) else Vertex(-1, "INVALID VERTEX")

    def __vertex_by_label(self, label: str) -> 'Vertex':
        """Retorna o Vertex especificado por rotulo."""
        try:
            return [ele for ele in self.__vertices if ele.get_label() == label][0]
        except IndexError:
            return Vertex(-1, "INVALID VERTEX")

    def vertex_index(self, label: str) -> int:
        """Retorna o indice do vertice especificado por rotulo"""
        return self.__vertex_by_label(label).get_idx()

    def vertex_label(self, idx: int) -> str:
        """Retorna o rotulo do vertice especificado por indice"""
        return self.__vertex_by_idx(idx).get_label()

    def n_vertices(self) -> int:
        """Retorna o numero de vertices do grafo."""
        return len(self.__vertices)

    def n_edges(self) -> int:
        """Retorna o numero de arestas que o grafo possui."""
        return len(self.__edges)

    def vertex_ngbrs(self, arg: Union[str, int]) -> "list[int]":
        """Retorna uma lista dos indices de vertices vizinhos ao vertice especificado."""
        if isinstance(arg, str):
            arg = self.vertex_index(arg)
        ngbrs = [ele.get_origin() for ele in self.__edges if ele.get_destiny() == arg] # arestas ngbr -> arg
        ngbrs.extend([ele.get_destiny() for ele in self.__edges if ele.get_origin() == arg]) # arestas arg -> ngbr
        ngbrs = list(dict.fromkeys(ngbrs)) # Remoção de duplicatas
        return ngbrs

    def vertex_ngbrs_label(self, arg: Union[str, int]) -> "list[str]":
        """Retorna uma lista dos rotulos de vertices vizinhos ao vertice especificado."""
        ngbrs = self.vertex_ngbrs(arg)
        ngbrs = [self.__vertex_by_idx(ele).get_label() for ele in ngbrs]

    def vertex_degree(self, arg: Union[str, int]) -> int:
        """Retorna o grau do vertice especificado por rotulo ou indice."""
        return len(self.vertex_ngbrs(arg)) if isinstance(arg, int) else len(self.vertex_ngbrs(self.vertex_index(arg)))

    def add_edge(self, vertex_a: Union[str, int], vertex_b: Union[str, int], weight: float):
        """Adiciona uma aresta entre os dois verticies especificados por rotulo ou indice com o peso indicado"""
        self.__edges.append(Edge(self.find_vertex(vertex_a).get_idx(), self.find_vertex(vertex_b).get_idx(), weight))
    
    def has_edge(self, vertex_a: Union[str, int], vertex_b: Union[str, int]) -> bool:
        """Retorna verdadeiro caso haja uma aresta entre os dois vertices especificados por rotulo ou indice"""
        if isinstance(vertex_a, str):
            vertex_a = self.vertex_index(vertex_a)
        if isinstance(vertex_b, str):
            vertex_b = self.vertex_index(vertex_b)

        return self.vertex_ngbrs(vertex_a).count(vertex_b) > 0

    def edge_weight(self, vertex_a: Union[str, int], vertex_b: Union[str, int]) -> Union[int, float]:
        """Retorna o peso de uma aresta entre a e b, preferencialmente de a -> b. Em caso de não existencia retorna uma representação de float('int')"""
        if isinstance(vertex_a, str):
            vertex_a = self.vertex_index(vertex_a)
        if isinstance(vertex_b, str):
            vertex_b = self.vertex_index(vertex_b)

        if self.has_edge(vertex_a, vertex_b):
            for element in self.__edges: 
                if element.get_origin() == vertex_a and element.get_destiny() == vertex_b:
                    return element.get_weight()
                elif element.get_origin() == vertex_b and element.get_destiny() == vertex_a:
                    return element.get_weight()

        return float('inf')

    def breadth_first_search(self, s: Union[str, int]) -> None:
        """Realiza uma busca em largura no grafo a partir do vertice s e imprime os resultados"""
        if isinstance(s, str):
            s = self.vertex_index(s)
        if s == -1 or s < 0 or s > len(self.__vertices):
            print("Error finding the root vertex.\n")
            return

        it = 0
        ngbrs = [s]
        all_until_now = [s]

        while True:
            print(f"{it}: {ngbrs[0]}", end='')
            for i in range(1, len(ngbrs)):
                all_until_now.append(ngbrs[i])
                print(f",{ngbrs[i]}", end='')

            next_ngbrs = []
            for ele in ngbrs:
                temp = self.vertex_ngbrs(ele)
                for val in temp:
                    if all_until_now.count(val) == 0:
                        all_until_now.append(val)
                        next_ngbrs.append(val)
            
            print()
            ngbrs = next_ngbrs
            it += 1
            if len(ngbrs) == 0:
                break
        print()

    def euler_cycle(self) -> None:
        """Procura pelo ciclo de euler do grafo pelo algoritmo de Hierholzer e imprime os resultados"""
        if not self.__has_euler_cycle():
            print("0")
            return
        else:
            c = [False]*len(self.__edges)
            found, cycle, c = self.__search_subcycle_euler(1, c)

            if not found:
                print("0")
                return
            else:
                if c.count(False) > 0:
                    print("0")
                    return
                else:
                    print("1")
                    print(f"{cycle[0]}", end="")
                    for i in range(1,len(cycle)):
                        print(f",{cycle[i]}", end="")
                    print()
                    return

    def __has_euler_cycle(self) -> bool:
        """Retorna verdadeiro se o grafo possuir um ciclo Euleriano"""
        for ele in self.__vertices:
            n_ngbrs = len(self.vertex_ngbrs(ele.get_idx()))
            if n_ngbrs == 0:
                return False
            elif n_ngbrs % 2:
                return False
        return True

    def __edge_pos(self, vertex_a: Union[str, int], vertex_b: Union[str, int]) -> int:
        """Retorna qual o índice do vetor de arestas possui um elemento que conecta vertex_a e vertex_b"""
        if isinstance(vertex_a, str):
            vertex_a = self.vertex_index(vertex_a)
        if isinstance(vertex_b, str):
            vertex_b = self.vertex_index(vertex_b)

        if not self.has_edge(vertex_a, vertex_b):
            return -1
        else:
            for i in range(len(self.__edges)):
                ori = self.__edges[i].get_origin()
                des = self.__edges[i].get_destiny()
                if  (des == vertex_a and ori == vertex_b) or (des == vertex_b and ori == vertex_a):
                    return i

    def __all_edges_pos(self, vertex_a: Union[str, int]) -> "list[int]":
        """Retorna uma lista com o índice de todas as arestas do vertex_a"""
        if isinstance(vertex_a, str):
            vertex_a = self.vertex_index(vertex_a)

        vec = []
        for ele in self.__vertices:
            if ele.get_idx() != vertex_a and self.has_edge(vertex_a, ele.get_idx()):
                vec.append(self.__edge_pos(vertex_a, ele.get_idx()))
        return vec

    def __search_subcycle_euler(self, v: int, c: "list[bool]") -> Tuple[bool, "list[int]", "list[bool]"]:
        """Procura por um subciclo de Euler dentro do grafo"""
        cycle = [v]
        t = 0
        first = True
        while v != t:
            if first:
                first = False
                t = v
            v_edges = self.__all_edges_pos(v)
            non_visited = [ele for ele in v_edges if not c[ele]]
            if len(non_visited) == 0:
                return False, [], []
            else:
                edge = self.__edges[non_visited[0]]
                c[non_visited[0]] = True
                v = edge.get_destiny() if edge.get_destiny() != v else edge.get_origin()
                cycle.append(v)

        for x in range(len(cycle)):
            x_edges = self.__all_edges_pos(cycle[x])
            non_visited = [ele for ele in x_edges if not c[ele]]
            if len(non_visited) > 0:
                found, subcycle, c = self.__search_subcycle_euler(cycle[x], c)
                if not found:
                    return False, [], c
                
                for i in range(len(subcycle)-1, -1, -1):
                    cycle.insert(x+1, subcycle[i])
                cycle.pop(x)

        return True, cycle, c

    def bellman_ford(self, s: Union[str, int]) -> None:
        pass

    def dijkstra(self, s: Union[str, int]) -> None:
        distancia = []
        if isinstance(s, str):
            vertex_indice = self.vertex_index(s)
        else: 
            vertex_indice = s

        for i in range(1, self.n_vertices() + 1):
            if i == vertex_indice:
                distancia.append([0.0, i, None, False])
            else:
                distancia.append([float('inf'), i, None, False])

        visitados = []
        vertex_selecionado = []
        while len(visitados) != self.n_vertices():
            
            vertex_selecionado = distancia[0]

            for element in distancia:
                if vertex_selecionado[3] == True:
                    vertex_selecionado = element
                elif element[3] == False and vertex_selecionado[0] > element[0]:
                    vertex_selecionado = element

            visitados.append(element)
            vertex_selecionado[3] = True
            
            for vertex_ngbrs in distancia:
                if vertex_ngbrs[1] in self.vertex_ngbrs(vertex_selecionado[1]) and vertex_ngbrs[3] == False:
                    if vertex_ngbrs[0] > vertex_selecionado[0] + self.edge_weight(vertex_ngbrs[1], vertex_selecionado[1]):
                        vertex_ngbrs[0] = vertex_selecionado[0] + self.edge_weight(vertex_ngbrs[1], vertex_selecionado[1])
                        vertex_ngbrs[2] = vertex_selecionado[1]
                    
        '''
        1: 2,3,4,1; d=7
        2: 2; d=0
        3: 2,3; d=4
        4: 2,3,4; d=6
        5: 2,3,5; d=8
        '''

        representation = ''
        for element in distancia:
            if element[2] == None:
                representation += '\n' + str(element[1]) + ': ' + str(element[1]) + '; d=' + ("%.0f" % element[0])
            else:
                representation += '\n' + str(element[1]) + ': '
                arrAux = [element[1]]
                anterior = element[2]
                index = 0
                while True:
                    index = index % len(distancia)

                    if distancia[index][1] == anterior:
                        arrAux.insert(0, anterior)
                        anterior = distancia[index][2]
                    if anterior == None:
                        break
                    
                    index += 1
                
                representation += ','.join([str(_) for _ in arrAux]) + '; d=' + ("%.0f" % element[0])


        print(representation)



    def adjacency_matrix(self) -> "list[int][int]":
        matrix = [None]*self.n_vertices()

        for i in range (len(matrix)):
            matrix[i] = [None]*self.n_vertices()

        for indexA in range(self.n_vertices()):
            for indexB in range(self.n_vertices()):
                if indexA == indexB:
                    matrix[indexA][indexB] = 0
                else:
                    matrix[indexA][indexB] = self.edge_weight(indexA + 1, indexB + 1)
                
        return matrix

    def floyd_warshall(self) -> None:
        
        graph = self.adjacency_matrix()

        for k in range(self.n_vertices()):
            for i in range(self.n_vertices()):
                for j in range(self.n_vertices()):
                    graph[i][j] = min(graph[i][j], graph[i][k] + graph[k][j])

        representation = ''
        for indexA in range(self.n_vertices()):
            for indexB in range(self.n_vertices()):
                if indexB == 0:
                    representation += '\n' + str(indexA + 1) + ': ' + ("%.0f" % graph[indexA][indexB])
                else:
                    representation += ',' + ("%.0f" % graph[indexA][indexB])
        
        print(representation)

class Vertex:
    def __init__(self, idx: int, label: str) -> None:
        self.__idx = idx
        self.__label = label

    def get_idx(self) -> int:
        """Retorna o indice do vertice"""
        return self.__idx

    def get_label(self) -> str:
        """Retorna o rotulo do vertice"""
        return self.__label

class Edge:
    def __init__(self, vertex_a: int, vertex_b: int, weight: float) -> None:
        """Cria uma aresta indo de vertex_a para vertex_b com peso weight"""
        self.__vertex_a = vertex_a
        self.__vertex_b = vertex_b
        self.__weight = weight

    def get_origin(self) -> 'Vertex':
        """Retorna o indice do vertice de origem."""
        return self.__vertex_a

    def get_destiny(self) -> 'Vertex':
        """Retorna o indice do vertice de destino."""
        return self.__vertex_b

    def get_weight(self) -> float:
        """Retorna o peso da aresta."""
        return self.__weight
