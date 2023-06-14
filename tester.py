from matplotlib import pyplot as plt

class Tester:

    tests = []

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

        for test in self.tests:

            averages = test.average_results
            indices = list(range(len(test.average_results)))
            plt.plot(indices, averages, marker='o')
            plt.xlabel('Generation')
            plt.ylabel('Fitness Score')
            plt.title('Fitness Score vs. Generation')
            plt.grid(True)
            plt.show()





class Test:

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
        self.fitness_results = []
        self.average_results = []

