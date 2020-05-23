# Compiler
CC := gcc -std=c99

# Options
CFLAGS := -Wall -Werror

# Dependencies
DEPS := util.h

# Objects
OBJS := util.o source.o

%.o: %.c $(DEPS)
	$(CC) $(FLAG) -c $<

a.exe: $(OBJS)
	$(CC) -o $@ $^

clean:
	$(RM) *.o *.exe