all: main testOutput submitOutput

CXX_FLAGS=-Wall -Wextra -pedantic --std=c++11

main: main.cpp
	g++ $(CXX_FLAGS) main.cpp -o main

testOutput: testInput main
	./main < testInput > testOutput

submitOutput: submitInput main
	./main < submitInput > submitOutput

clean:
	rm -rf main testOutput submitOutput
