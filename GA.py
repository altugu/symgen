import random
from MeshGraph import *


class GA:
    def __init__(self, mesh, error_function):
        self.population_size = mesh.number_of_vertices
        self.vertices = mesh.vertices
        self.faces = mesh.faces
        self.right_samples = mesh.right_samples_indices
        self.left_samples = mesh.left_samples_indices
        self.target = []
        self.error_function = error_function
        self.distances_1 = mesh.distances_1
        self.distances_2 = mesh.distances_2
        self.detected_symmetry_count = 0
        self.next_generation = mesh.right_samples_indices
        self.max_generations = 1000  # any value
        self.isPaired = [False] * len(mesh.left_samples_indices)
        self.fixed_point1 = mesh.input1
        self.fixed_point2 = mesh.input2
        print("GA")
        self.geneticAlgorithm()

    def point_position(self, point):
        if(point.z < self.fixed_point1.z and point.z < self.fixed_point2.z ):
            return "Left"
        elif (point.z > self.fixed_point1.z and point.z > self.fixed_point2.z ):
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

    def absolute_error(self, distance1, distance2):

        return abs(distance2 - distance1)

    def squared_error(self, distance1, distance2):
        return (distance2 - distance1) ** 2

    def relative_error(self, distance1, distance2):
        return abs(distance2 - distance1) / distance1

    def relative_squared_error(self, distance1, distance2):
        return ((distance2 - distance1) ** 2) / (distance1 ** 2)

    def crossover(self, index):
        pass

    def mutation(self, index):
        self.next_generation[index] = random.randint(0, self.population_size)

    def evaluateFitness(self, index, right, left):
        error = self.error_function(self, self.distances_1[right], self.distances_1[left]) + self.error_function(
            self, self.distances_2[right], self.distances_2[left])
        prob = random.random()
        #print(str(right) + " :")
        #print(self.vertices[right] )
        if(error < 0.0001 and self.point_position(self.vertices[right]) == "Right"):
            self.isPaired[index] = True
            self.detected_symmetry_count += 1
        else:
            if(prob > 0.5):
                self.mutation(index)  # to be changed
            else:
                self.mutation(index)  # to be changed

        return error

    def getPairs(self):
        true_indexes = [index for index,
                        value in enumerate(self.isPaired) if value]
        result = [(self.left_samples[index], self.right_samples[index])
                  for index in true_indexes]
        return result

    def geneticAlgorithm(self):

        for GENERATION in range(self.max_generations):
            self.right_samples = self.next_generation
            fitness_score = 0
            for index, (right, left) in enumerate(zip(self.right_samples, self.left_samples)):
                if(self.isPaired[index] == True):
                    continue
                fitness_score += self.evaluateFitness(index, right, left)
            #print(f"generation: {GENERATION + 1}  fitness: {fitness_score}")
        print(self.detected_symmetry_count)
