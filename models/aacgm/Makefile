all: clean compile

clean:
	-rm test_aacgm

compile:
	gcc -Wall -o test_aacgm test_aacgm.c aacgmlib_v2.c AstAlg.c -lm -static
