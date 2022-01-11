#include <stdio.h>
#include <string.h>
int main(){
    char * buff [32];
    char str [32] = "here is some stuff";
    strcpy(buff, str);
    printf("The address of buff is : %p \n", buff);
    printf("the address of str is : %p \n", str);
    printf("str contains: %s \n",str);
}