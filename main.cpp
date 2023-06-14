

#include "Mesh.h"
#include <fstream>
#include <iostream>
#include <string>

using namespace std;

void writeSamplesToFile(Mesh* mesh, char *file_name) {
    std::vector<int>& samples = mesh->samples;  // Assuming mesh->samples is a vector of integers

    // Open the file
    const char* dir = "sampled_points/";

    // Determine the length of the strings
    size_t dir_len = strlen(dir);
    size_t filename_len = strlen(file_name);

    // Create a char array with enough space for the concatenated strings
    char filepath[dir_len + filename_len + 1];  // +1 for the null-terminator

    // Copy the directory to the filepath
    strcpy(filepath, dir);

    // Concatenate the filename to the filepath
    strcat(filepath, file_name);
    std::ofstream file(filepath);

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
    char* sample_file_name = argv[2];
    sample_mesh->loadOff(file_name, Load_option::withoutColor);
    sample_mesh->computeCenterOfMass();
    sample_mesh->findNearestMeshtoCom(true, Color(255,0,0));
    sample_mesh->computeEvenlySpacedSamples(200, false, Color(0, 255, 0));
    sample_mesh->outputWithBrush();
    
    writeSamplesToFile(sample_mesh, sample_file_name);
    
    return 0;
}
