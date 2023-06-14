import math
import random
from MeshGraph import *
import matplotlib.pyplot as plt
import statistics
from tester import Tester, Test

class GA:
    target = []
    def __init__(self,
                 mesh,
                 error_function,
                 max_generation=1000,
                 mutation_prob_threshold=0.1,
                 errors_z_value_threshold=2.7,
                 tester=None
                 ):
        self.tester = tester
        self.test = Test(
            error_function=error_function,
            max_generation=max_generation,
            mutation_prob_threshold=mutation_prob_threshold,
            errors_z_value_threshold=errors_z_value_threshold
        )
        self.errors_z_value_threshold = errors_z_value_threshold
        self.mutation_prob_threshold = mutation_prob_threshold
        self.population_size = mesh.n_vertices
        self.vertices = mesh.vertices
        self.faces = mesh.faces
        self.right_samples_indices = mesh.right_samples_indices
        self.left_samples_indices = mesh.left_samples_indices
        self.error_function = error_function
        self.distances_1 = mesh.distances_1
        self.distances_2 = mesh.distances_2

        self.detected_symmetry_count = 0
        self.next_generation = mesh.right_samples_indices
        self.max_generation = max_generation  # any value
        self.isPaired = [False] * len(mesh.left_samples_indices)
        self.fixed_point1 = mesh.input1_vertex
        self.fixed_point2 = mesh.input2_vertex
        print("GA")
        self.test.start_time()
        self._geneticAlgorithm()
        self.test.end_time()
        self.tester.addTest(self.test)

    def _geneticAlgorithm(self):
        fitness_scores = []
        for GENERATION in range(self.max_generation):
            self.right_samples_indices = self.next_generation
            errors = []
            for index, (left, right) in enumerate(zip(self.left_samples_indices, self.right_samples_indices)):
                if self.isPaired[index]:
                    continue
                errors.append(self.evaluateErrors(right, left))
            normalized_errors = self.normalize_errors(errors)
            fitness_score = self.evaluateFitnessScore(normalized_errors)
            fitness_scores.append(fitness_score)

        self.test.fitness_results.append(fitness_scores)

        print(self.detected_symmetry_count)

    def crossover(self, index):
        rand_index = random.randint(0, len(self.right_samples_indices) - 1)
        self.next_generation[index] = self.right_samples_indices[rand_index]
        self.next_generation[rand_index] = self.right_samples_indices[index]

    def mutation(self, index):

        cand_vertex_index = random.randint(0, self.population_size - 1)
        self.next_generation[index] = cand_vertex_index
        while self.point_position(self.vertices[cand_vertex_index]) != "Right":
            cand_vertex_index = random.randint(0, self.population_size - 1)
            self.next_generation[index] = cand_vertex_index

    def normalize_errors(self, errors):
        threshold = self.errors_z_value_threshold  # Adjust the threshold as needed

        mean = statistics.mean(errors)
        std_dev = statistics.stdev(errors)

        filtered_errors = [error for error in errors if abs((error - mean) / std_dev) <= threshold]

        if len(filtered_errors) == 0:
            min_val = min(errors)
            max_val = max(errors)
            normalized_errors = [(error - min_val) / (max_val - min_val) for error in errors]
        else:
            min_val = min(filtered_errors)
            max_val = max(filtered_errors)
            normalized_errors = [(error - min_val) / (max_val - min_val) for error in filtered_errors]


        return normalized_errors
    def evaluateErrors(self, right, left):
        error = self.error_function(self, self.distances_1[right], self.distances_1[left]) + self.error_function(
            self, self.distances_2[right], self.distances_2[left])
        return error

    def evaluateFitnessScore(self, normalized_errors):

        fitness_score = 0
        for index, norm_error in enumerate(normalized_errors):
            related_pair = (self.left_samples_indices[index], self.right_samples_indices[index])
            prob = random.random()
            if norm_error < 0.001 and self.point_position(self.vertices[related_pair[1]]) == "Right":
                self.isPaired[index] = True
                self.detected_symmetry_count += 1
            elif prob > self.mutation_prob_threshold:
                self.mutation(index)  # to be changed # to be changed
                fitness_score += norm_error
            else:
                self.crossover(index)
        return fitness_score

    def getPairs(self):
        true_indexes = [index for index,
                        value in enumerate(self.isPaired) if value]
        result = [(self.left_samples_indices[index], self.right_samples_indices[index])
                  for index in true_indexes]
        return result

    def point_position(self, point):
        if point.z < self.fixed_point1.z and point.z < self.fixed_point2.z:
            return "Left"
        elif point.z > self.fixed_point1.z and point.z > self.fixed_point2.z:
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

    def absolute_error(self, distance1, distance2):

        return abs(distance2 - distance1)

    def squared_error(self, distance1, distance2):
        return (distance2 - distance1) ** 2

    def relative_error(self, distance1, distance2):
        if distance1 == 0:
            return math.inf
        return abs(distance2 - distance1) / distance1

    def relative_squared_error(self, distance1, distance2):
        if distance1 == 0:
            return math.inf
        return ((distance2 - distance1) ** 2) / (distance1 ** 2)
