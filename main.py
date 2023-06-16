
from MeshGraph import *
from GA import *
from tester import *
import sys
import time

# targetPhrase = "vicarious"
# popMax = 400
# mutationRate = 0.03
#
# nature = Nature(targetPhrase, mutationRate, popMax)
#
# x = False
# while(x == False):
#     x = nature.iterateOneGeneration()

def absolute_error( distance1, distance2):

    return abs(distance2 - distance1)
def naiveApproach(mesh, count):
    left_samples = mesh.left_samples_indices[:count]
    vertices = mesh.vertices
    for sample in left_samples:
        for vertex in vertices:
            if(mesh.point_position(vertex) == "Right"):
                left_d_1 = mesh.distances_1[sample]
                left_d_2 = mesh.distances_2[sample]

                right_d_1 = mesh.distances_1[vertex.collection_index]
                right_d_2 = mesh.distances_2[vertex.collection_index]
                error =0
                error += absolute_error(left_d_1, right_d_1)
                error += absolute_error(left_d_2,right_d_2)
                if(error < 0.0001):
                    continue

def readInputFile(filePath):
    with open(f'{filePath}', 'r') as file:
        line = file.readline()

    input_tuple = tuple(map(int, line.split()))
    print(input_tuple)
    return input_tuple
def main():

    tester = Tester()
    # Example usage
    fileName = sys.argv[1]
    inputFile = sys.argv[2]
    sampleFile = sys.argv[3]
    input = readInputFile(inputFile)
    #fileName = "1.off"
    tester.rootPath = fileName
    mesh = MeshGraph(fileName, input)
    print(mesh.input1_vertex, mesh.input2_vertex)
    error_functions = [
        GA.absolute_error,
        GA.relative_error,
        GA.squared_error,
        GA.relative_squared_error
    ]
    max_generations = {
        800
    }

    for max_generation in max_generations:
        for error_function in error_functions:
            print(f"error function: {error_function.__name__}")
            ga = GA(mesh=mesh,
                    error_function=error_function,
                    max_generation=max_generation,
                    mutation_prob_threshold=0.1,
                    errors_z_value_threshold=3.0,
                    tester=tester
                    )
            pairs = ga.getPairs()
            mesh.brushPair(pairs)
            
            mesh.meshToFile(f"{os.path.basename(mesh.filePath)}_{error_function.__name__}.off")

    tester.show_results()

    pair_count = len(pairs)
    
    start_time = time.time()
    naiveApproach(mesh, pair_count)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Naive execution time: {execution_time} seconds")

main()
