
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


def printForMesh(mesh):
    print("Vertices")
    print(mesh.getVertices()[:5])
    print(len(mesh.getVertices()))

    print("Edges")
    print(mesh.getEdges()[:5])
    print(len(mesh.getEdges()))

    print("Faces")
    print(mesh.getFaces()[:5])
    print(len(mesh.getFaces()))

    print("Face[0] neighbors")
    x = mesh.getFaces()

    for index, face in enumerate(x):
        print(f"NEIGHBOR FACES OF FACE-{index}")
        if len(face.neighbor_faces_triple) != 3:
            print(f"ERROR - {len(face.neighbor_faces_triple)}")
            break
    print("FINISH")


def main():

    # Example usage
    fileName = "1.off"
    mesh = MeshGraph(fileName)
    printForMesh(mesh)
    mesh.meshToFile("MERT.off")



    #ga = GA(vertices=mesh.vertices, faces=mesh.faces,right_samples=mesh.right_samples_indices, left_samples=mesh.left_samples_indices)
    # Assuming vertices and faces are populated with the required data

    # Perform uniform sampling with 10 samples
    #mesh.uniform_sampling(24, "uniform_0")
    #symmetries = mesh.findIntrinsicSymmetricPoints("uniform_0")

    #mesh.setColorVertices(mesh.uniform_samples["uniform_0"])


main()



