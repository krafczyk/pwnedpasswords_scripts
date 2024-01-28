all: search_hash_with_progress.so

search_hash_with_progress.so: search_hash_with_progress.cpp
	g++ -O3 -Wall -shared -std=c++11 -fPIC $^ -o $@
