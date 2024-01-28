// file: search_hash_with_progress.cpp

#include <iostream>
#include <fstream>
#include <string>
#include <chrono>


std::string get_hash_at_position(std::ifstream &file, long long position) {
    std::string line;

    // Seek to the position
    file.seekg(position);

    // Move back to the start of the line
    if (position != 0) {
        char ch;
        while (file.get(ch)) {
            if (ch == '\n') {
                break;
            }
            file.seekg(-2, std::ios_base::cur);
        }
    }

    // Read the line
    if (std::getline(file, line)) {
        return line;  // Return the complete line
    }

    return "";  // Return empty string if line is not found
}


std::string binary_search_hash(std::ifstream &file, const std::string &target_hash) {
    long long left = 0;
    file.seekg(0, std::ios::end);
    long long right = file.tellg();

    while (left <= right) {
        long long mid = left + (right - left) / 2;
        std::string line = get_hash_at_position(file, mid);

        size_t colon_pos = line.find(':');
        if (colon_pos != std::string::npos) {
            std::string current_hash = line.substr(0, colon_pos);
            if (current_hash == target_hash) {
                return line;  // Hash found
            }

            if (current_hash < target_hash) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
    }

    return "";  // Hash not found
}


extern "C" {
    int search_hash(const char* file_path, const char* hash) {
        static std::string result;
        std::ifstream file(file_path);
        if (!file.is_open()) {
            result = "File not open";
            return -1;
        }

        result = binary_search_hash(file, hash);

        file.close();

        // Get number of occurances for the hash.
        size_t colon_pos = result.find(':');
        if (colon_pos != std::string::npos) {
            // Get the remainder of the line and turn it into an int.
            int num_occurances = std::stoi(result.substr(colon_pos + 1));
            return num_occurances;
        } else {
            return -2;
        }
    }
}
