This program is a simplified version of the Unix “diff” program in assembly. It compares the lines one by one and implements the -i and -b options.

The "diff.c" and "diff-main.c" files have been given as a framework for the assignment.

They give the following signature:
int diff(FILE *a, FILE *b, bool i_flag, bool B_flag);

Wecan assume that no line is longer than 1024 characters.

The assembly program is written in the diff-frame.S.
To compile, run `gcc -o diff diff-main.c diff-frame.S -g`.
To run, use `./diff`.
