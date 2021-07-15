from typing import Union

class Graph:
    def __init__(self, file: str) -> None:
        self.__vertices: "list['Vertex']" = []
        self.__edges: "list['Edge']" = []
        self.__load_file(file)

    def __load_file(self, file: str) -> None:
        data = open(file, 'r')
        lines = data.readlines()

        for line in lines:
            sp_line = line.split()
            if len(sp_line) == 2 and sp_line[0] != "*vertices":
                self.__vertices.append(Vertex(int(sp_line[0]), sp_line[1]))
            elif len(sp_line) == 3:
                self.__edges.append(Edge(int(sp_line[0]), int(sp_line[1]), float(sp_line[2])))

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
            edges = [ele for ele in self.__edges if ele.get_origin() == vertex_a]
            if any(edges):
                return edges[0].get_weight()
            else:
                edges = [ele for ele in self.__edges if ele.get_origin() == vertex_b]
                if any(edges):
                    return edges[0].get_weight()

        return float('inf')

    def breadth_first_search(self, s: Union[str, int]) -> None:
        """Realiza uma busca em largura no grafo a partir do vertice s e imprime os resultados em tela"""
        if isinstance(s, str):
            s = self.vertex_index(s)
        if s == -1 or s < 0 or s > len(self.__vertices):
            print("Error finding the root vertex.")
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

    def euler_cycle(self) -> None:
        pass

    def bellman_ford(self, s: Union[str, int]) -> None:
        pass

    def dijkstra(self, s: Union[str, int]) -> None:
        pass

    def floyd_Warshall(self) -> None:
        pass

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
