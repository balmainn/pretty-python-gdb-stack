#include <stdio.h>
#include <string.h>
int function(){
    printf("in function");
    return 1;
}
int main(){
    char * m = malloc(sizeof(char));
    char * buff [32];
    int t = function();
    printf("function: %d\n", t);
    char str [32] = "here is some stuff";
    strcpy(buff, str);
    printf("The address of buff is : %p \n", buff);
    printf("the address of str is : %p \n", str);
    printf("str contains: %s \n",str);
    int end = 0;
}