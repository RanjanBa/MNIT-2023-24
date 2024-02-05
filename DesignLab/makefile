CC = gcc
CFLAGS = -Wall
LDFLAGS = 
OBJFILES = add.o subtract.o multiply.o division.o main.o
TARGET = test
all: $(TARGET)

$(TARGET): $(OBJFILES)
	$(CC) $(CFLAGS) -o $(TARGET) $(OBJFILES) $(LDFLAGS)
clean:
	rm -f $(OBJFILES) $(TARGET)