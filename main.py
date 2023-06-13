
from MeshGraph import *
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
    mesh = MeshGraph(fileName)
    center_point = mesh.vertices[int(mesh.com[0][0])]
    print(center_point.x, center_point.y, center_point.z)
    #sample_point = mesh.vertices[7000]
    #print(sample_point)
    print(mesh.vertices[int(mesh.com[0][2])])
    mesh.shortestPath( center_point, mesh.distances_1)
    mesh.writeFileSplit()
    print(mesh.distances_1[mesh.vertices[int(mesh.com[0][2])].collection_index])
    print(len(mesh.right_samples_indices))
    print(mesh.right_samples_indices)
    print(mesh.left_samples_indices)

    #ga = GA(vertices=mesh.vertices, faces=mesh.faces,right_samples=mesh.right_samples_indices, left_samples=mesh.left_samples_indices)
    # Assuming vertices and faces are populated with the required data

    # Perform uniform sampling with 10 samples
    #mesh.uniform_sampling(24, "uniform_0")
    #symmetries = mesh.findIntrinsicSymmetricPoints("uniform_0")

    #mesh.setColorVertices(mesh.uniform_samples["uniform_0"])


main()

