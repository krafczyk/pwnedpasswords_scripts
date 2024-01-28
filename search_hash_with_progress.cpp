// file: search_hash_with_progress.cpp

#include <iostream>
#include <fstream>
#include <string>

extern "C" {
    typedef void (*ProgressCallback)(long);

    int search_hash_with_progress(const char* file_path, const char* hash, ProgressCallback progress_callback) {
        std::ifstream file(file_path);
        if (!file.is_open()) {
            return -1;
        }

        std::string line;
        long bytes_read = 0;
        while (std::getline(file, line)) {
            bytes_read += line.length() + 1; // Include newline character
            progress_callback(bytes_read);

            size_t colon_pos = line.find(':');
            if (colon_pos != std::string::npos) {
                std::string current_hash = line.substr(0, colon_pos);
                if (current_hash == hash) {
                    // Get the remainder of the line and turn it into an int.
                    int num_occurances = std::stoi(line.substr(colon_pos + 1));
                    file.close();
                    return num_occurances;
                }
            }
        }

        file.close();
        return -2;
    }
}
