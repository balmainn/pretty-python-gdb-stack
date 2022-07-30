#include <stdio.h>
#include <malloc.h>

int A;
int B;

int function(int depth) {
    int rc;
    char buf[5];
    char *stuff = (char *) malloc(16*sizeof(char));

    if(depth < 10)
        rc = function(depth+1);
	else
		rc = 0;

	free(stuff);

    return rc;
}

int main(int argc, char* argv[]) {
    int x;
    char *buffer = (char *) malloc(128*sizeof(char));
    int  *array = (int *) malloc(128*sizeof(int));

    x = function(0);

    return 0;
}
