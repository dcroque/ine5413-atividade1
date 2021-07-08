from typing import NewType

class Graph:
    def __init__(self, file: str) -> None:
        self.__load_file(file)

    def __load_file(self, file: str):
        # open file
        a = len(file)

        # read vertices
        for i in range (a):
            self.__vertices = []

        # read edges
        for i in range (a):
            self.__edges = []

class Vertex:
    def __init__(self, idx: int, label: str) -> None:
        self.__idx = idx
        self.__label = label
        self.__edges = []

    def get_idx(self) -> int:
        return self.__idx

    def get_label(self) -> str:
        return self.__label

    def get_ngbrs(self) -> list['Edge']:
        return self.__edges

    def get_ngbrs_label(self) -> list[int]:
        return [element.get_vertex().get_label() for element in self.__edges]

    def get_ngbrs_idx(self) -> list[str]:
        return [element.get_vertex().get_idx() for element in self.__edges]

    def add_edge(self, edge: 'Edge') -> None:
        self.__edges.append(edge)

class Edge:
    def __init__(self, vertex: 'Vertex', weight: int) -> None:
        self.__vertex = vertex
        self.__weight = weight

    def get_vertex(self) -> 'Vertex':
        return self.__vertex

    def get_weight(self) -> int:
        return self.__weight
