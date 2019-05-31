CC = gcc
CFLAGS = -g -Wall -O2

CFILES =  y.tab.c

OFILES =  y.tab.o table.o tree.o

compile: $(OFILES)
	$(CC) $(CFLAGS) $(OFILES) -lfl -o compile

table.o : table.c tableandtree.h
	$(CC) $(CFLAGS) -c -o table.o table.c

tree.o : tree.c tableandtree.h
	$(CC) $(CFLAGS) -c -o tree.o tree.c

y.tab.o : lex.yy.c y.tab.h y.tab.c tableandtree.h table.o tree.o
	$(CC) $(CFLAGS) -c -o y.tab.o y.tab.c

lex.yy.c : scanner.l
	flex $^

y.tab.c : parser_subset1.y
	yacc $^

y.tab.h : parser_subset1.y
	yacc -d -v $^

.PHONY: clean
clean:
	/bin/rm -f compile lex.yy.c *.o y.tab.c y.tab.h y.output
