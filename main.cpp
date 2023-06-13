

#include "Mesh.h"
#include <fstream>
#include <iostream>
#include <string>

using namespace std;

void writeSamplesToFile(Mesh* mesh) {
    std::vector<int>& samples = mesh->samples;  // Assuming mesh->samples is a vector of integers

    // Open the file
    std::ofstream file("sampled_1.txt");

    // Check if the file is open and writable
    if (file.is_open()) {
        // Write each element of the samples vector to the file
        for (const int& sample : samples) {
            file << sample << "\n";  // Write each integer on a new line
        }

        // Close the file
        file.close();
    } else {
        // Failed to open the file
        std::cout << "Unable to open the file." << std::endl;
    }
}

int main(int argc, char ** argv)
{   

    cout << "working..." << endl;

    Mesh* sample_mesh = new Mesh(false, 1);

    char* file_name =  argv[1];
    sample_mesh->loadOff(file_name, Load_option::withoutColor);
    sample_mesh->computeCenterOfMass();
    sample_mesh->findNearestMeshtoCom(true, Color(255,0,0));
    sample_mesh->computeEvenlySpacedSamples(100, false, Color(0, 255, 0));
    sample_mesh->outputWithBrush();
    
    writeSamplesToFile(sample_mesh);
    
    return 0;
}
