all: search_hash.so

search_hash.so: search_hash.cpp
	g++ -O3 -Wall -shared -std=c++11 -fPIC $^ -o $@
