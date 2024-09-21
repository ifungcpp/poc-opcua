# Makefile for building OPC UA Client

# Compiler
CXX = g++

# Compiler flags
CXXFLAGS = -std=c++11 -I../github/open62541/include

# Source files
SRC = tutorial_client_firststeps.c

# Output executable
TARGET = tutorial_client_firststeps.x

# Build target
all: $(TARGET)

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(SRC) -L../github/open62541/lib -lopen62541

# Clean target
clean:
	rm -f $(TARGET)
