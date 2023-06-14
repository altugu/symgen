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
        self.vertice_1 = vertice_1
        self.vertice_2 = vertice_2
        self.vertice_3 = vertice_3
        self.collection_index = index
        self.neighbour12 = None
        self.neighbour13 = None
        self.neighbour23 = None
    

    def __str__(self):
        str_return = f"""
            FACE_INDEX:{self.collection_index}\n\n
            vertice_1:\n    {self.vertice_1} 
            vertice_2:\n    {self.vertice_2} 
            vertice_3:\n    {self.vertice_3} 
            color:\n    {self.color}
        """
        return str_return

    def toTuple(self):
        return self.vertice_1.index, self.vertice_2.index, self.vertice_3.index


class MeshGraph:

    def __init__(self, filePath,input):
        self.filePath = filePath
        self.uniform_samples = {}
        self.uniform_counter = 0
        self.vertices = []
        self.faces = []
        self._readFromFile(filePath)
        self.number_of_vertices = len(self.vertices)
        self.number_of_faces = len(self.faces)
        self.center_of_mass = self.calculateCenterOfMass()
        self.center_vertex = self.calculateCenterVertex()
        
        
        #LATER ADDITIONS
        self.distances_1 = [math.inf] * (self.number_of_vertices+1)
        self.distances_2 = [math.inf] * (self.number_of_vertices+1)
        self.evenly_sampled_points = []
        self.com = []
        self._readModifiedFile(filePath)
        self.right_samples_indices = []
        self.left_samples_indices = []
        self.samples = []
        #self.middle_vertex = self.vertices[int(self.com[0][0])]
        self.readSamplesFromFile("sampled_1.txt")
        self.input1 =  self.vertices[input["input1"]]
        self.input2 = self.vertices[input["input2"]]

        self.splitSamples()
    
    def readSamplesFromFile(self,file_path):
        with open(file_path, 'r') as file:
            for line in file:
                sample = int(line.strip())
                self.samples.append(sample)
        
    def splitSamples(self):
        for sample in self.samples:
            vertex = self.vertices[sample]
            pos = self.point_position(vertex)
            if(pos == "Right"):
                self.right_samples_indices.append(sample)
            elif(pos == "Left"):
                self.left_samples_indices.append(sample)

    def point_position(self, point):
        if(point.z < self.input1.z and point.z < self.input2.z ):
            return "Left"
        elif (point.z > self.input1.z and point.z > self.input2.z ):
            return "Right"
        else:
            return "On the Rectangle"
        #Below code for line seperation
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
    def calculateCenterVertex(self):
        min_dist = math.inf
        min_vertex_index = None
        for index_vertex, vertex in enumerate(self.vertices):
            sum_sqr = math.pow(vertex.x - self.center_of_mass[0], 2)\
                      + math.pow(vertex.y - self.center_of_mass[1],2)\
                      + math.pow(vertex.z - self.center_of_mass[2], 2)
            dist = math.sqrt(sum_sqr)
            if dist < min_dist:
                min_dist = dist
                min_vertex_index = index_vertex

        return min_vertex_index

    def calculateCenterOfMass(self):

        sum_x = 0
        sum_y = 0
        sum_z = 0
        for vertex in self.vertices:
            sum_x += vertex.x
            sum_y += vertex.y
            sum_z += vertex.z

        avr_x = sum_x / self.number_of_vertices
        avr_y = sum_y / self.number_of_vertices
        avr_z = sum_z / self.number_of_vertices

        return avr_x, avr_y, avr_z

    def uniform_sampling(self, num_samples, key):
        # Create a sampling pool
        sampling_pool = []

        # Add indices of all faces to the sampling pool
        for vertex in self.vertices:
            sampling_pool.append(vertex.collection_index)

        # Sample the desired number of indices from the sampling pool
        sampled_indices = random.sample(sampling_pool, num_samples)
        uniform_samples_value = []
        for index in sampled_indices:
            uniform_samples_value.append(self.vertices[index])
        self.uniform_samples[key] = uniform_samples_value
        self.uniform_counter += 1

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
                    calc_distance = distance_list[current_vertex.collection_index] + self.euclidianDistance(current_vertex, neighbor_vertex) 
                    if( calc_distance < distance_list[neighbor_vertex.collection_index] ):
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
            meshInfo =  meshLines[1]
            self.n_vertices, self.n_faces, self.n_edges = meshInfo.split(sep=" ")

            face_index = 0
            # vertices and faces
            for vertice_index, meshLine in enumerate(meshLines[2:]):

                meshInfo = list (map(float,  meshLine[:-1].split(sep=" ") ))

                # vertice
                if (len(meshInfo) == 7):
                    if(meshInfo[4:] == [255,0,0]):
                        self.com.append(meshInfo[1:4])
                    else:
                        self.evenly_sampled_points.append(meshInfo[1:4])

    def writeFileSplit(self):
        with open("split.off", "w") as file:
            file.write("OFF\n")
            file.write("12500 24998 37497\n")

            for index in range(self.number_of_vertices):
                vertex = self.vertices[index]
                file.write(str(vertex.x) + " " + str(vertex.y) +" " + str(vertex.z) + "\n")
            
            for index in range(self.number_of_faces):
                face = self.faces[index]
                vertex = face.vertice_1

                if (face.color != None):
                    center_point = self.vertices[int(self.com[0][0])]
                    if (vertex.z > center_point.z):
                        face.color = [172,42,44]
                file.write("3 "+ str(face.vertice_1.collection_index)+ " " + str(face.vertice_2.collection_index) + " " + str(face.vertice_3.collection_index))
                if (face.color):
                    file.write(" " + str(face.color[0])+ " " + str(face.color[1]) +" " +str(face.color[2]) + " ")
                file.write("\n")


    def _readFromFile(self, filePath):

        with open(filePath, "r") as meshFile:

            meshLines = meshFile.readlines()
            meshInfo = meshLines[1]

            self.n_vertices, self.n_faces, self.n_edges = meshInfo.split(sep=" ")

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
                    n_index = int(meshInfo[0])
                    vertice_index_lst = [int(i) for i in meshInfo[1:]]

                    vertice_1 = self.vertices[vertice_index_lst[0]]
                    vertice_2 = self.vertices[vertice_index_lst[1]]
                    vertice_3 = self.vertices[vertice_index_lst[2]]
                    color = None
                    if(len(meshInfo) == 7):
                        color = vertice_index_lst[3:]


                    face = Face(vertice_1, vertice_2, vertice_3, face_index)

                    vertice_1.addInvolvedFace(face)
                    vertice_2.addInvolvedFace(face)
                    vertice_3.addInvolvedFace(face)

                        

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
            added_str = (f'3 {face.vertice_1.collection_index} {face.vertice_2.collection_index} {face.vertice_3.collection_index}')
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
            v1,v2 = self.vertices[pair[0]],self.vertices[ pair[1]]
            color = (random.randint(0,128), random.randint(128,256), random.randint(0,256))
            for face in v1.involved_faces:
                face.color = color            
            for face in v2.involved_faces:
                face.color = color

            
    def get_neighbor_indices(self, vertex):

        neighbor_indices = []
        for face in vertex.involved_faces:
            if face.vertice_1.collection_index != vertex.collection_index:
                neighbor_indices.append(face.vertice_1)
            if face.vertice_2.collection_index != vertex.collection_index:
                neighbor_indices.append(face.vertice_2)
            if face.vertice_3.collection_index != vertex.collection_index:
                neighbor_indices.append(face.vertice_3)

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
