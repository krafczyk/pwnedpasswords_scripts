// file: search_hash_with_progress.cpp

#include <iostream>
#include <fstream>
#include <string>
#include <chrono>

extern "C" {
    typedef void (*ProgressCallback)(long);

    int search_hash_with_progress(const char* file_path, const char* hash, ProgressCallback progress_callback) {
        std::ifstream file(file_path);
        if (!file.is_open()) {
            return -1;
        }

        // Set up timing for callbacks
        auto start = std::chrono::steady_clock::now();
        long wait_ms = 100;
        int i = 0;
        int N = 1000;

        std::string line;
        long bytes_read = 0;
        while (std::getline(file, line)) {
            bytes_read += line.length() + 1; // Include newline character

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

            // If we've look at enough hashes, check the time
            i += 1;
            if (i == N) {
                // 
                i = 0;
                auto end = std::chrono::steady_clock::now();
                long elapsed_ms = std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count();
                // Check if its been enough time for a callback
                if (elapsed_ms > wait_ms) {
                    start = end;
                    progress_callback(bytes_read);
                }
            }
        }

        file.close();
        return -2;
    }
}
