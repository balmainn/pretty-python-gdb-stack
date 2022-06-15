#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main( int argc, char *argv[]){
    printf("%d, %s", argc, argv[0]);   

    // for (int i = 0; i < argc ; i ++){
    //     printf("%d: %s: %d: \n", i, argv[i], atoi(argv[i]));
    // }
    char procfilepath[20];
    strcpy(procfilepath,"/proc/");
    strcat(procfilepath,argv[1]);
    strcat(procfilepath, "/stat");
    //char procfilepath[16] = "/proc/self/stat";
    printf("%s", procfilepath);

    FILE *fp = fopen(procfilepath,"r");
    char buff[2048];
    for (int i = 0; i < 52; i++){
        fscanf(fp, "%s", buff);
        printf("%d: string: %s lu:%lu\n",i, buff );
        
    }
    
    fclose(fp);
 //cat /proc/{procnospace}/stat').read()   
}