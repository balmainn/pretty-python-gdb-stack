#include <stdio.h>
#include <string.h>
#include <stdlib.h>
int function(){
    printf("in function");
    int functionVar = 3;
    return 1;
}
int main(){
    char * m = malloc(sizeof(char));
    char * buff [32];
    int t = function();
    printf("function: %d\n", t);
    char str [32] ;
    strcpy(str, "here is some stuff");
    strcpy(buff, str);
    strcpy(m, str);
    printf("The address of buff is : %p \n", buff);
    printf("the address of str is : %p \n", str);
    printf("str contains: %s \n",str);
    int end = 0;
}