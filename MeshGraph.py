import numpy as np
import random
import math
from queue import Queue


def compare_with_margin(value1, value2, margin_percentage):
    margin = margin_percentage / 100 * value1
    diff = abs(value1 - value2)
    return diff <= margin


class Vertex:


    def __init__(self, x, y, z, index):
        self.x, self.y, self.z = x, y, z
        self.collection_index = index
        self.involved_faces = []

    def __str__(self):
        str_return = f"""
            VERTEX_INDEX: {self.collection_index}
            x: {self.x}
            y: {self.y}
            z: {self.z}
        """

        return str_return

    def addInvolvedFace(self, face):
        self.involved_faces.append(face)

class Face:
    color = None

    def __init__(self, vertice_1, vertice_2, vertice_3, index):
        self.vertex_1 = vertice_1
        self.vertex_2 = vertice_2
        self.vertex_3 = vertice_3
        self.collection_index = index
        self.neighbour12 = None
        self.neighbour13 = None
        self.neighbour23 = None

    def __str__(self):
        str_return = f"""
            FACE_INDEX:{self.collection_index}\n\n
            vertice_1:\n    {self.vertex_1} 
            vertice_2:\n    {self.vertex_2} 
            vertice_3:\n    {self.vertex_3} 
            color:\n    {self.color}
        """
        return str_return

    def toTuple(self):
        return self.vertex_1.index, self.vertex_2.index, self.vertex_3.index


class MeshGraph:
    vertices = []
    n_vertices = 0

    faces = []
    n_faces = 0

    n_edges = 0

    input1_vertex = None
    input2_vertex = None
    com = []
    evenly_sampled_points = []

    right_samples_indices = []
    left_samples_indices = []
    samples = []

    def __init__(self, filePath, input, withColor=False):
        self.withColor = withColor
        self.filePath = filePath
        self._readFromFile(filePath)

        # LATER ADDITIONS
        self.input1_vertex = self.vertices[input[0]]
        self.input2_vertex = self.vertices[input[1]]
        self.distances_1 = [math.inf] * (self.n_vertices + 1)
        self.distances_2 = [math.inf] * (self.n_vertices + 1)
        self.shortestPath(self.input1_vertex, self.distances_1)
        self.shortestPath(self.input2_vertex, self.distances_2)

        self._readModifiedFile(filePath)

        # self.middle_vertex = self.vertices[int(self.com[0][0])]
        self.readSamplesFromFile("sampled_1.txt")
        self.splitSamples()

        right_sample_size = len(self.right_samples_indices)
        if len(self.left_samples_indices) < right_sample_size:
            self.left_samples_indices += [0] * (right_sample_size - len(self.left_samples_indices))
        else:
            self.left_samples_indices = self.left_samples_indices[:right_sample_size]

    def splitSamples(self):
        for sample in self.samples:
            vertex = self.vertices[sample]
            pos = self.point_position(vertex)
            if (pos == "Right"):
                self.right_samples_indices.append(sample)
            elif (pos == "Left"):
                self.left_samples_indices.append(sample)

    def point_position(self, point):
        if point.z < self.input1_vertex.z and point.z < self.input2_vertex.z:
            return "Left"
        elif point.z > self.input1_vertex.z and point.z > self.input2_vertex.z:
            return "Right"
        else:
            return "On the Rectangle"
        # Below code for line seperation
        '''
        vector1 = [self.input2.x - self.input1.x, self.input2.z - self.input1.z]
        vector2 = [point.x - self.input1.x, point.z - self.input1.z]

      
        cross_product = vector1[0] * vector2[1] - vector1[1] * vector2[0]

        if cross_product > 0:
            return "Left"
        elif cross_product < 0:
            return "Right"
        else:
            return "On the line"
        '''

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

    def euclidianDistance(self, vertex1, vertex2):
        return math.sqrt((vertex1.x - vertex2.x) ** 2 + (vertex1.y - vertex2.y) ** 2 + (vertex1.z - vertex2.z) ** 2)

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
            for neighbor_vertex in self.get_neighbor_indices(current_vertex):
                if not visited[neighbor_vertex.collection_index]:
                    queue.put(neighbor_vertex)
                    visited[neighbor_vertex.collection_index] = True
                    parent[neighbor_vertex.collection_index] = current_vertex
                    calc_distance = distance_list[current_vertex.collection_index] + self.euclidianDistance(
                        current_vertex, neighbor_vertex)
                    if (calc_distance < distance_list[neighbor_vertex.collection_index]):
                        distance_list[neighbor_vertex.collection_index] = calc_distance

        # If no path is found, return an empty list
        return []

    def toString(self, head=False):
        str_return = str()
        str_return += "vertices\n"

        vertices = self.vertices[:5] if head else self.vertices
        faces = self.faces[:5] if head else self.faces
        for i in vertices:
            str_return += str(type(i)) + "\n"
            str_return += str(i) + "\n"
        str_return += "faces\n"
        for j in faces:
            str_return += str(type(j)) + "\n"
            str_return += str(j) + "\n"

        return str_return

    def _readModifiedFile(self, filePath):
        with open(filePath, "r") as meshFile:

            meshLines = meshFile.readlines()

            face_index = 0
            # vertices and faces
            for vertice_index, meshLine in enumerate(meshLines[2:]):

                meshInfo = list(map(float, meshLine[:-1].split(sep=" ")))

                # vertice
                if (len(meshInfo) == 7):
                    if (meshInfo[4:] == [255, 0, 0]):
                        self.com.append(meshInfo[1:4])
                    else:
                        self.evenly_sampled_points.append(meshInfo[1:4])

    def readSamplesFromFile(self, file_path):
        with open(file_path, 'r') as file:
            for line in file:
                sample = int(line.strip())
                self.samples.append(sample)

    def writeFileSplit(self):
        with open("split.off", "w") as file:
            file.write("OFF\n")
            file.write("12500 24998 37497\n")

            for index in range(self.n_vertices):
                vertex = self.vertices[index]
                file.write(str(vertex.x) + " " + str(vertex.y) + " " + str(vertex.z) + "\n")

            for index in range(self.n_faces):
                face = self.faces[index]
                vertex = face.vertex_1

                if (face.color != None):
                    center_point = self.vertices[int(self.com[0][0])]
                    if (vertex.z > center_point.z):
                        face.color = [172, 42, 44]
                file.write(
                    "3 " + str(face.vertex_1.collection_index) + " " + str(face.vertex_2.collection_index) + " " + str(
                        face.vertex_3.collection_index))
                if (face.color):
                    file.write(" " + str(face.color[0]) + " " + str(face.color[1]) + " " + str(face.color[2]) + " ")
                file.write("\n")

    def _readFromFile(self, filePath):

        with open(filePath, "r") as meshFile:

            meshLines = meshFile.readlines()
            meshInfo = meshLines[1]

            self.n_vertices, self.n_faces, self.n_edges = [int(i) for i in meshInfo.split(sep=" ")]
            print(self.n_vertices)
            print(type(self.n_vertices))
            print([int(i) for i in meshInfo.split(sep=" ")])

            face_index = 0
            # vertices and faces
            for vertice_index, meshLine in enumerate(meshLines[2:]):

                meshInfo = meshLine[:-1].split(sep=" ")

                # vertice
                if (len(meshInfo) == 3):
                    meshInfo = [float(i) for i in meshInfo]
                    vertice = Vertex(meshInfo[0], meshInfo[1], meshInfo[2], vertice_index)
                    self.vertices.insert(vertice_index, vertice)

                else:
                    vertex_index_lst = [int(i) for i in meshInfo[1:]]

                    vertex_1 = self.vertices[vertex_index_lst[0]]
                    vertex_2 = self.vertices[vertex_index_lst[1]]
                    vertex_3 = self.vertices[vertex_index_lst[2]]
                    color = None
                    if len(meshInfo) == 7 and self.withColor:
                        color = vertex_index_lst[3:]

                    face = Face(vertex_1, vertex_2, vertex_3, face_index)
                    face.color = color
                    vertex_1.addInvolvedFace(face)
                    vertex_2.addInvolvedFace(face)
                    vertex_3.addInvolvedFace(face)

                    self.faces.insert(face_index, face)

                    face_index += 1

    def meshToFile(self, fileName):
        last_string = (
            'OFF\n'
            '12500 24998 0\n'
        )

        for vertex in self.vertices:
            added_str = f'{vertex.x} {vertex.y} {vertex.z}\n'
            last_string += added_str
        for face in self.faces:
            added_str = (
                f'3 {face.vertex_1.collection_index} {face.vertex_2.collection_index} {face.vertex_3.collection_index}')
            if face.color != None:
                added_str += f' {int(face.color[0])} {int(face.color[1])} ' \
                             f'{int(face.color[2])}\n'
            else:
                added_str += '\n'
            last_string += added_str

        with open(fileName, "w") as file:
            file.write(last_string)
            file.truncate()

    def brushPair(self, pairs):
        for pair in pairs:
            v1, v2 = self.vertices[pair[0]], self.vertices[pair[1]]
            color = (random.randint(0, 128), random.randint(128, 256), random.randint(0, 256))
            for face in v1.involved_faces:
                face.color = color
            for face in v2.involved_faces:
                face.color = color

    def get_neighbor_indices(self, vertex):

        neighbor_indices = []
        for face in vertex.involved_faces:
            if face.vertex_1.collection_index != vertex.collection_index:
                neighbor_indices.append(face.vertex_1)
            if face.vertex_2.collection_index != vertex.collection_index:
                neighbor_indices.append(face.vertex_2)
            if face.vertex_3.collection_index != vertex.collection_index:
                neighbor_indices.append(face.vertex_3)

        return neighbor_indices

    def setColorVertices(self, lst_vertices):

        with open(self.filePath, "r") as meshFile:

            root_mesh_lines = meshFile.readlines()

            mesh_start = root_mesh_lines[:2]
            mesh_lines = root_mesh_lines[2:]

            mesh_vertices = [i for i in mesh_lines if len(i.split(" ")) == 3]
            mesh_faces = [i for i in mesh_lines if len(i.split(" ")) == 4]

            print(mesh_lines)
            print(mesh_vertices)
            print(mesh_faces)

            for vertex in lst_vertices:
                faces = vertex.involved_faces
                for face in faces:
                    face_index = face.collection_index
                    mesh_faces[face_index] = mesh_faces[face_index][:-1] + " 255 255 0\n"

            last_mesh_lines = mesh_start + mesh_vertices + mesh_faces

        with open(self.filePath[:-4] + "_modified.off", "w") as meshFile:
            meshFile.write("".join(last_mesh_lines))
