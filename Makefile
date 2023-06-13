CC = g++
CFLAGS = -std=c++11 -Wall

all: main

main: main.o Mesh.o
	$(CC) $(CFLAGS) $^ -o $@

Main.o: main.cpp Mesh.h
	$(CC) $(CFLAGS) -c $<

Mesh.o: Mesh.cpp Mesh.h FibHeap.h
	$(CC) $(CFLAGS) -c $<

clean:
	rm -f *.o main