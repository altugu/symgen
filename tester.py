from matplotlib import pyplot as plt

import time


class Tester:
    tests = []
    tests_time_result = []

    def addTest(self, test):
        self.tests.append(test)

    def show_results(self):
        if len(self.tests) == 0:
            return
        for test in self.tests:
            # Calculate the average for each index
            print(test.fitness_results)
            transposed_results = list(map(list, zip(*test.fitness_results)))
            averages = [sum(values) / len(test.fitness_results) for values in transposed_results]
            test.average_results = averages

        for index, test in enumerate(self.tests):
            averages = test.average_results
            indices = list(range(len(test.average_results)))
            plt.plot(indices, averages, marker='o')
            plt.xlabel('Generation')
            plt.ylabel('Fitness Score')
            plt.title(f'Genetic Algorithm - {index}')
            plt.suptitle((''
                          f'MAX_GEN: {test.max_generation}  -  '
                          f'Z_VALUE_TH: {test.errors_z_value_threshold}  -  '
                          f'ERROR_FUNC: {test.error_function.__name__}\n'
                          f'AVR_TIME: {test.time_passed}ms')
                         )
            plt.grid(True)
            plt.show()


class Test:
    start_time = 0  # s
    end_time = 0  # s
    time_passed = 0  # ms
    fitness_results = []
    average_results = []

    def __init__(self,
                 error_function,
                 max_generation,
                 mutation_prob_threshold,
                 errors_z_value_threshold
                 ):
        self.error_function = error_function
        self.max_generation = max_generation
        self.mutation_prob_threshold = mutation_prob_threshold
        self.errors_z_value_threshold = errors_z_value_threshold

    def start_time(self):
        self.start_time = time.time()

    def end_time(self):
        self.end_time = time.time()
        self.time_passed = round((self.end_time - self.start_time) * 1000, 4)
