
from MeshGraph import *
from GA import *
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

    # Example usage
    fileName = sys.argv[1]
    input = {"input1": 5158,
             "input2": 11573}
    mesh = MeshGraph(fileName, input)

    #sample_point = mesh.vertices[7000]
    # print(sample_point)
    mesh.shortestPath(mesh.input1, mesh.distances_1)
    mesh.shortestPath(mesh.input2, mesh.distances_2)
    # mesh.writeFileSplit()


    size = len(mesh.right_samples_indices)
    if len(mesh.left_samples_indices) < size:
        mesh.left_samples_indices += [0] * (size - len(mesh.left_samples_indices))
    else:
        mesh.left_samples_indices = mesh.left_samples_indices[:size]
    #print(mesh.point_position(mesh.input1, mesh.input2, mesh.vertices[9548]))
    print(len(mesh.right_samples_indices))
    print(len(mesh.left_samples_indices))
    ga = GA(mesh=mesh, error_function=GA.squared_error)

    print(ga.point_position(mesh.vertices[9861]))
    # Assuming vertices and faces are populated with the required data

    # Perform uniform sampling with 10 samples
    #mesh.uniform_sampling(24, "uniform_0")
    #symmetries = mesh.findIntrinsicSymmetricPoints("uniform_0")

    # mesh.setColorVertices(mesh.uniform_samples["uniform_0"])
    pairs = ga.getPairs()
    dashLine = "-" * 150

    for pair in pairs:

        vertex1 = mesh.vertices[pair[0]]
        vertex2 = mesh.vertices[pair[1]]

        delta = 0.01
        print(f"((x0<{vertex1.x + delta})&& (x0>{vertex1.x - delta})&&(y0<{vertex1.y + delta})&&(y0>{vertex1.y - delta})&&(z0<{vertex1.z + delta})&&(z0>{vertex1.z - delta}))||((x0<{vertex2.x + delta})&& (x0>{vertex2.x - delta})&&(y0<{vertex2.y + delta})&&(y0>{vertex2.y - delta})&&(z0<{vertex2.z + delta})&&(z0>{vertex2.z - delta}))")
        print(dashLine)
    mesh.brushPair(pairs)
    mesh.meshToFile("mesh63_paired.off")
    #left_vertex = mesh.vertices[pairs[1][0]]
    #right_vertex = mesh.vertices[pairs[1][1]]
    #print(left_vertex, right_vertex)
    #delta = 0.01
    #dashLine = "-" * 50
    # print(f"(x0=={left_vertex.x})&&(y0=={left_vertex.y})&&(z0<{left_vertex.z})")
    # print(dashLine)
    #print(f"(x<{left_vertex.x + delta})&& (x>{left_vertex.x - delta})&&(y<{left_vertex.y + delta})&&(y>{left_vertex.y - delta})&&(z<{left_vertex.z + delta})&&(z>{left_vertex.z - delta})")
    #print(f"(x0<{left_vertex.x + delta})&& (x0>{left_vertex.x - delta})&&(y0<{left_vertex.y + delta})&&(y0>{left_vertex.y - delta})&&(z0<{left_vertex.z + delta})&&(z0>{left_vertex.z - delta})")
    # print(dashLine)
    #print(f"(x<{right_vertex.x + delta})&& (x>{right_vertex.x - delta})&&(y<{right_vertex.y + delta})&&(y>{right_vertex.y - delta})&&(z<{right_vertex.z + delta})&&(z>{right_vertex.z - delta})")
    #print(f"(x0<{right_vertex.x + delta})&& (x0>{right_vertex.x - delta})&&(y0<{right_vertex.y + delta})&&(y0>{right_vertex.y - delta})&&(z0<{right_vertex.z + delta})&&(z0>{right_vertex.z - delta})")


main()
