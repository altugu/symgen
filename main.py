
from MeshGraph import *
from GA import *
from tester import *
import sys
# targetPhrase = "vicarious"
# popMax = 400
# mutationRate = 0.03
#
# nature = Nature(targetPhrase, mutationRate, popMax)
#
# x = False
# while(x == False):
#     x = nature.iterateOneGeneration()


def main():

    tester = Tester()
    # Example usage

    fileName = "1.off"
    input = (5158,11573)
    mesh = MeshGraph(fileName, input)
    print(mesh.input1_vertex, mesh.input2_vertex)
    error_functions = [
        GA.squared_error,
        GA.absolute_error,
        GA.relative_error,
        GA.relative_squared_error
    ]

    for error_function in error_functions:
        print(f"error function: {error_function.__name__}")
        ga = GA(mesh=mesh,
                error_function=error_function,
                max_generation=1000,
                mutation_prob_threshold=0.1,
                errors_z_value_threshold=3.0,
                tester=tester
                )
        pairs = ga.getPairs()
        print(len(pairs))
        mesh.brushPair(pairs)
        mesh.meshToFile(f"1_{error_function.__name__}.off")

    tester.show_results()



main()
