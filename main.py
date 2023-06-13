
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
    input = {"input1": 7195,
             "input2": 11573}
    mesh = MeshGraph(fileName,input)


    center_point = mesh.vertices[int(mesh.com[0][0])]
    print(center_point.x, center_point.y, center_point.z)
    #sample_point = mesh.vertices[7000]
    # print(sample_point)
    print(mesh.vertices[int(mesh.com[0][2])])
    mesh.shortestPath(mesh.input1, mesh.distances_1)
    mesh.shortestPath(mesh.input2, mesh.distances_2)
    # mesh.writeFileSplit()
    print(mesh.distances_1[mesh.vertices[int(
        mesh.com[0][2])].collection_index])
    print(len(mesh.right_samples_indices))
    print(len(mesh.left_samples_indices))
    
    #print(mesh.point_position(mesh.input1, mesh.input2, mesh.vertices[9548]))
    
    ga = GA(mesh=mesh, error_function=GA.squared_error)
    print(ga.point_position(mesh.vertices[7959]))
    # Assuming vertices and faces are populated with the required data

    # Perform uniform sampling with 10 samples
    #mesh.uniform_sampling(24, "uniform_0")
    #symmetries = mesh.findIntrinsicSymmetricPoints("uniform_0")

    # mesh.setColorVertices(mesh.uniform_samples["uniform_0"])
    #pairs = ga.getPairs()
    #vertex1 = mesh.vertices[pairs[0][0]]
    #vertex2 = mesh.vertices[pairs[0][1]]
    #for face in vertex1.involved_faces:
    #    print(face)    
    #for face in vertex2.involved_faces:
    #    print(face)
    #left_vertex = mesh.vertices[pairs[1][0]]
    #right_vertex = mesh.vertices[pairs[1][1]]
    #print(left_vertex, right_vertex)
    #delta = 0.01
    #dashLine = "-" * 50
    ##print(f"(x0=={left_vertex.x})&&(y0=={left_vertex.y})&&(z0<{left_vertex.z})") 
    #print(dashLine)
    #print(f"(x<{left_vertex.x + delta})&& (x>{left_vertex.x - delta})&&(y<{left_vertex.y + delta})&&(y>{left_vertex.y - delta})&&(z<{left_vertex.z + delta})&&(z>{left_vertex.z - delta})")
    #print(f"(x0<{left_vertex.x + delta})&& (x0>{left_vertex.x - delta})&&(y0<{left_vertex.y + delta})&&(y0>{left_vertex.y - delta})&&(z0<{left_vertex.z + delta})&&(z0>{left_vertex.z - delta})") 
    #print(dashLine)
    #print(f"(x<{right_vertex.x + delta})&& (x>{right_vertex.x - delta})&&(y<{right_vertex.y + delta})&&(y>{right_vertex.y - delta})&&(z<{right_vertex.z + delta})&&(z>{right_vertex.z - delta})")
    #print(f"(x0<{right_vertex.x + delta})&& (x0>{right_vertex.x - delta})&&(y0<{right_vertex.y + delta})&&(y0>{right_vertex.y - delta})&&(z0<{right_vertex.z + delta})&&(z0>{right_vertex.z - delta})")


main()
