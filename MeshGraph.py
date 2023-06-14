import numpy as np
import random
import math
from queue import Queue
import json

print_flag = 0


def tprint(string):
    if print_flag: print(string)


def compare_with_margin(value1, value2, margin_percentage):
    margin = margin_percentage / 100 * value1
    diff = abs(value1 - value2)
    return diff <= margin


class Vertex:
    involved_faces = []
    involved_edges = []
    neighbor_vertices = []

    def __init__(self, x, y, z, index):
        self.x, self.y, self.z = x, y, z
        self.collection_index = index

    def __str__(self):
        str_return = f"""
            VERTEX_INDEX: {self.collection_index}
            x: {self.x}
            y: {self.y}
            z: {self.z}
        """

        return str_return

    def getIndex(self):
        return self.collection_index

    def addInvolvedFace(self, face):
        if face not in self.involved_faces:
            self.involved_faces.append(face)
        else:
            return False

    def addInvolvedEdges(self, edge):
        if edge not in self.involved_edges:
            self.involved_edges.append(edge)
        else:
            return False

    def addNeighborVertex(self, vertex):
        if vertex not in self.neighbor_vertices:
            self.neighbor_vertices.append(vertex)
        else:
            return False

    def getInvolvedFaces(self):
        return self.involved_faces

    def getInvolvedEdges(self):
        return self.involved_edges

    def getNeighborVertices(self):
        return self.neighbor_vertices

    @staticmethod
    def vertexDistance(vertex_1, vertex_2):
        x_diff = abs(vertex_1.x - vertex_2.x)
        y_diff = abs(vertex_1.y - vertex_2.y)
        z_diff = abs(vertex_1.z - vertex_2.z)
        return math.sqrt(math.pow(x_diff, 2) + math.pow(y_diff, 2) + math.pow(z_diff, 2))


class Edge:
    involved_faces_pair = []

    def __init__(self, vertex_1, vertex_2, key):
        self.key = key
        self.vertex_pair = (vertex_1, vertex_2)
        self.length = Vertex.vertexDistance(vertex_1, vertex_2)

    def __str__(self):
        str_return = f"""
            EDGE:\n
            vertice_1:\n    {self.vertex_pair[0]} 
            vertice_2:\n    {self.vertex_pair[1]} 
            \n 
        """
        return str_return

    def addInvolvedFace(self, face):
        length = len(self.involved_faces_pair)
        if length == 0:
            self.involved_faces_pair.append(face)
        elif length == 1:
            self.involved_faces_pair.append(face)
            self.involved_faces_pair = tuple(self.involved_faces_pair)


    def getVertices(self): return self.vertex_pair

    def getVertex_0(self): return self.vertex_pair[0]

    def getVertex_1(self): return self.vertex_pair[1]

    def getLength(self): return self.length

    def getKey(self): return self.key

    def getInvolvedFacesPair(self):
        return self.involved_faces_pair

    def to_dict(self):
        return {
            'key': self.key,
            'vertex_pair': [v.to_dict() for v in self.vertex_pair],
        }

    def to_json(self):
        return json.dumps(self.to_dict())


class Face:
    neighbor_faces_triple = []
    edge_triple = []
    color = -1

    def __init__(self, vertex_1, vertex_2, vertex_3, key):
        self.key = key
        self.vertex_triple = (vertex_1, vertex_2, vertex_3)

    def __str__(self):
        str_return = f"""
            FACE:\n\n
            vertice_1:\n    {self.getVertex_0()} 
            vertice_2:\n    {self.getVertex_1()} 
            vertice_3:\n    {self.getVertex_2()} 
            color:\n    {self.color}
        """
        return str_return

    def addNeighborFace(self, face):
        self.neighbor_faces_triple.append(face)
        if len(self.neighbor_faces_triple) == 3:
            self.neighbor_faces_triple = tuple(self.neighbor_faces_triple)
    def getNeigborFaces(self): return self.neighbor_faces_triple

    def getVertices(self): return self.vertex_triple

    def getVertex_0(self): return self.vertex_triple[0]

    def getVertex_1(self): return self.vertex_triple[1]

    def getVertex_2(self): return self.vertex_triple[2]

    def getEdges(self): return self.edge_triple

    def setEdges(self, edges):
        self.edge_triple = (edges[0], edges[1], edges[2])

    def getKey(self): return self.key

    def setColor(self, color): self.color = color


    def to_dict(self):
        return {
            'key': self.key,
            'vertex_triple': [v.to_dict() for v in self.vertex_triple],
        }

    def to_json(self):
        return json.dumps(self.to_dict())

class MeshGraph:
    vertices = []
    faces = {}
    edges = {}

    def __init__(self, filePath):
        self.filePath = filePath
        print("starting reading of file...")
        self._readFromFile(filePath)
        self.number_of_vertices = len(self.vertices)
        self.number_of_edges = len(self.edges)
        self.number_of_faces = len(self.faces)

        # LATER ADDITIONS
        print("starting later additions...")
        self.distances_1 = [math.inf] * self.number_of_vertices
        self.distances_2 = [math.inf] * self.number_of_vertices
        self.evenly_sampled_points = []
        self.right_samples_indices = []
        self.left_samples_indices = []
        self.samples = []
        self._readSamplesFromFile("sampled_1.txt")

    def getVertices(self):
        return self.vertices

    def getFaces(self):
        return list(self.faces.values())

    def getEdges(self):
        return list(self.edges.values())

    def _readSamplesFromFile(self, file_path):
        with open(file_path, 'r') as file:
            for line in file:
                sample = int(line.strip())
                self.samples.append(sample)

    def splitSamples(self, split_points):
        return

    # self.left_samples_indices = [sample for sample in self.samples if
    #                              self.vertices[sample].z < self.center_of_mass[2]]
    # self.right_samples_indices = [sample for sample in self.samples if
    #                               self.vertices[sample].z > self.center_of_mass[2]]

    def uniform_sampling(self, num_samples, key):
        return

    # # Create a sampling pool
    # sampling_pool = []
    #
    # # Add indices of all faces to the sampling pool
    # for vertex in self.vertices:
    #     sampling_pool.append(vertex.collection_index)
    #
    # # Sample the desired number of indices from the sampling pool
    # sampled_indices = random.sample(sampling_pool, num_samples)
    # uniform_samples_value = []
    # for index in sampled_indices:
    #     uniform_samples_value.append(self.vertices[index])

    def findIntrinsicSymmetricPoints(self, uniform_sample_key):
        '''
            x sample icin
            (x*(x-1))/2 tane karsilastirma

            O(x^2)

            allahini seven optimize etsin

        :return:
        '''

        counter = 0
        pairs = []
        uniform_samples_lst = self.uniform_samples[uniform_sample_key]
        for index_1, vertex_1 in enumerate(uniform_samples_lst):
            path_1 = self.shortestPath(vertex_1, self.center_vertex)
            length_1 = len(path_1)
            print(index_1)
            for index_2, vertex_2 in enumerate(uniform_samples_lst[index_1 + 1:]):
                print(index_2)
                counter += 1
                path_2 = self.shortestPath(vertex_2, self.center_vertex)
                length_2 = len(path_2)

                if compare_with_margin(length_1, length_2, 0.2):
                    pairs.append([(vertex_1, length_1), (vertex_2, length_2)])

        print(pairs)
        print(f"Intrinsic Symmetry loop counter: {counter}")
        return pairs

    def shortestPath(self, from_vertex, distance_list):
        # Create a visited array to keep track of visited vertices
        visited = [False] * len(self.vertices)
        # Create a parent array to store the parent of each vertex in the shortest path
        parent = [-1] * len(self.vertices)

        # Perform BFS traversal
        queue = Queue()
        queue.put(from_vertex)

        visited[from_vertex.collection_index] = True
        distance_list[from_vertex.collection_index] = 0
        while not queue.empty():
            current_vertex = queue.get()
            '''
            if current_vertex == to_vertex:
                # Reached the destination, construct the path
                path = []
                while current_vertex != -1:
                    path.insert(0, current_vertex)
                    current_index = parent[current_vertex]
                return path
        '''
            # Explore the neighboring vertices
            for neighbor_vertex in current_vertex.getNeighborVertices():
                if not visited[neighbor_vertex.collection_index]:
                    queue.put(neighbor_vertex)
                    visited[neighbor_vertex.collection_index] = True
                    parent[neighbor_vertex.collection_index] = current_vertex
                    calc_distance = distance_list[current_vertex.collection_index] + \
                                    Vertex.vertexDistance(current_vertex, neighbor_vertex)
                    if calc_distance < distance_list[neighbor_vertex.collection_index]:
                        distance_list[neighbor_vertex.collection_index] = calc_distance

        # If no path is found, return an empty list
        return []

    def writeFileSplit(self):
        with open("split.off", "w") as file:
            file.write("OFF\n")
            file.write("12500 24998 37497\n")

            for index in range(self.number_of_vertices):
                vertex = self.vertices[index]
                file.write(str(vertex.x) + " " + str(vertex.y) + " " + str(vertex.z) + "\n")

            for index in range(self.number_of_faces):
                face = self.faces[index]
                vertex = face.vertice_1

                if (face.color != None):
                    center_point = self.vertices[int(self.com[0][0])]
                    if (vertex.z > center_point.z):
                        face.color = [172, 42, 44]
                file.write("3 " + str(face.vertice_1.collection_index) + " " + str(
                    face.vertice_2.collection_index) + " " + str(face.vertice_3.collection_index))
                if (face.color):
                    file.write(" " + str(face.color[0]) + " " + str(face.color[1]) + " " + str(face.color[2]) + " ")
                file.write("\n")

    def _readFromFile(self, filePath):

        with open(filePath, "r") as meshFile:
            mesh_lines = meshFile.readlines()

        mesh_info = mesh_lines[1]

        self.n_vertices, self.n_faces, self.n_edges = mesh_info.split(sep=" ")

        # vertices and faces
        for vertex_index, meshLine in enumerate(mesh_lines[2:]):

            meshInfo = meshLine[:-1].split(sep=" ")

            # vertice
            if len(meshInfo) == 3:
                print("Construction vertices...")
                self._add_vertice_from_meshInfo(meshInfo, vertex_index)
                print("Construction vertices end!")
            # face and edges
            else:
                print("Construction face, edges and involves...")
                self._add_face_edge_and_other_op(meshInfo)
                print("Construction face, edges and involes end!")

    def _add_face_edge_and_other_op(self, meshInfo):
        color = -1
        if len(meshInfo) == 7:
            lst = [int(i) for i in meshInfo[1:]]
            color = tuple(lst[-3:])
            vertex_index_lst = lst[1:-3]
        elif len(meshInfo) == 4:
            vertex_index_lst = [int(i) for i in meshInfo[1:]]

        vertex_1 = self.vertices[vertex_index_lst[0]]
        vertex_2 = self.vertices[vertex_index_lst[1]]
        vertex_3 = self.vertices[vertex_index_lst[2]]

        # edges created and added
        edge12 = self.add_edge(vertex_1, vertex_2)
        vertex_1.addNeighborVertex(vertex_2)
        vertex_2.addNeighborVertex(vertex_1)

        edge13 = self.add_edge(vertex_1, vertex_3)
        vertex_1.addNeighborVertex(vertex_3)
        vertex_3.addNeighborVertex(vertex_1)

        edge23 = self.add_edge(vertex_2, vertex_3)
        vertex_2.addNeighborVertex(vertex_3)
        vertex_3.addNeighborVertex(vertex_2)

        # face created and added
        face = self.add_face(vertex_1, vertex_2, vertex_3)
        # add edges to face
        face.setEdges((edge12, edge13, edge23))
        if color != -1:
            face.color = color
        # add face to edge
        edge12.addInvolvedFace(face)
        edge13.addInvolvedFace(face)
        edge23.addInvolvedFace(face)

        # add edges and face to vertex
        vertex_1.addInvolvedEdges(edge12)
        vertex_1.addInvolvedEdges(edge13)
        vertex_1.addInvolvedFace(face)

        vertex_2.addInvolvedEdges(edge12)
        vertex_2.addInvolvedEdges(edge23)
        vertex_2.addInvolvedFace(face)

        vertex_3.addInvolvedEdges(edge13)
        vertex_3.addInvolvedEdges(edge23)
        vertex_3.addInvolvedFace(face)


    def _add_vertice_from_meshInfo(self, meshInfo, vertex_index):
        meshInfo = [float(i) for i in meshInfo]
        vertex = Vertex(meshInfo[0], meshInfo[1], meshInfo[2], vertex_index)
        self.vertices.insert(vertex_index, vertex)

    # key = index_1 - index_2 - index_3 for face ----- index_1 - index_2 for edge
    def get_face_key(self, vertex_1, vertex_2, vertex_3):
        vertex_indices = list(sorted([vertex_1.collection_index, vertex_2.collection_index, vertex_3.collection_index]))
        key = '-'.join(map(str, vertex_indices))
        return key

    def add_face(self, vertex_1, vertex_2, vertex_3):
        key = self.get_face_key(vertex_1, vertex_2, vertex_3)
        if key not in self.faces:
            face = Face(vertex_1, vertex_2, vertex_3, key)
            self.faces[key] = face
            return face
        return False
        # Perform any additional operations you need for adding a face

    def get_edge_key(self, vertex_1, vertex_2):
        index1 = vertex_1.collection_index
        index2 = vertex_2.collection_index
        key = f"{min(index1, index2)}-{max(index1, index2)}"
        return key

    def add_edge(self, vertex_1, vertex_2):
        key = self.get_edge_key(vertex_1, vertex_2)
        if key not in self.edges:
            print("edge added...")
            edge = Edge(vertex_1, vertex_2, key)
            self.edges[key] = edge
            return edge
        print("edge grabbed...")
        return self.edges[key]
        # Perform any additional operations you need for adding an edge

    def getEdgeWithVertices(self, vertex_1, vertex_2):
        key = self.get_edge_key(vertex_1, vertex_2)
        if key in self.edges:
            return self.edges[key]
        return False

    def getFaceWithVertices(self, vertex_1, vertex_2, vertex_3):
        key = self.get_face_key(vertex_1, vertex_2, vertex_3)
        if key in self.faces:
            return self.faces[key]
        return False

    def setColorVertices(self, lst_vertices):

        with open(self.filePath, "r") as meshFile:

            root_mesh_lines = meshFile.readlines()

            mesh_start = root_mesh_lines[:2]
            mesh_lines = root_mesh_lines[2:]

            mesh_vertices = [i for i in mesh_lines if len(i.split(" ")) == 3]
            mesh_faces = [i for i in mesh_lines if len(i.split(" ")) == 4]

            for vertex in lst_vertices:
                faces = vertex.involved_faces
                for face in faces:
                    face_index = face.collection_index
                    mesh_faces[face_index] = mesh_faces[face_index][:-1] + " 255 255 0\n"

            last_mesh_lines = mesh_start + mesh_vertices + mesh_faces

        with open(self.filePath[:-4] + "_modified.off", "w") as meshFile:
            meshFile.write("".join(last_mesh_lines))

    def meshToFile(self, fileName):
        last_string = (
            'OFF\n'
            f'{self.number_of_vertices} {self.number_of_faces} {self.number_of_edges}\n'
        )

        for vertex in self.vertices:
            added_str = f'{vertex.x} {vertex.y} {vertex.z}\n'
            last_string += added_str
        for face in list(self.faces.values()):
            added_str = (f'3 {face.vertex_triple[0].collection_index} '
                         f'{face.vertex_triple[1].collection_index} '
                         f'{face.vertex_triple[2].collection_index}')
            if face.color != -1:
                added_str += f' {int(face.color[0])} {int(face.color[1])} ' \
                             f'{int(face.color[2])}\n'
            else:
                added_str += '\n'
            last_string += added_str

        with open(fileName, "w") as file:
            file.write(last_string)
            file.truncate()

    def to_dict(self):
        return {
            'vertices': [v.to_dict() for v in self.vertices],
            'edges': [e.to_dict() for e in self.edges.values()],
            'faces': [f.to_dict() for f in self.faces.values()],
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    def save_to_json(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.to_dict(), file)

    @classmethod
    def from_dict(cls, data):
        mesh_graph = cls.__new__(cls)
        mesh_graph.vertices = [Vertex(**v) for v in data['vertices']]
        mesh_graph.edges = {e['key']: Edge(Vertex(**v[0]), Vertex(**v[1]), e['key']) for e in data['edges']}
        mesh_graph.faces = {f['key']: Face(*[Vertex(**v) for v in f['vertex_triple']], f['key']) for f in data['faces']}
        return mesh_graph

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        return cls.from_dict(data)

    @classmethod
    def load_from_json(cls, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
        return cls.from_dict(data)

