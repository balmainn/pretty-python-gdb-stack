#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main( int argc, char *argv[]){
    //printf("%d, %s", argc, argv[0]);   

    // for (int i = 0; i < argc ; i ++){
    //     printf("%d: %s: %d: \n", i, argv[i], atoi(argv[i]));
    // }
    char procfilepath[20];
    strcpy(procfilepath,"/proc/");
    strcat(procfilepath,argv[1]);
    strcat(procfilepath, "/stat");
    //char procfilepath[16] = "/proc/self/stat";
    //printf("%s", procfilepath);

    FILE *fp = fopen(procfilepath,"r");
    char buff[2048];
    int useful_stack_info[] = {23,26,27,28,29,30,45,46,47,48,49,50,51,52};
    // for( int i =0; i < 10; i++){
    //     printf("%d: \n", useful_stack_info[i]);
    // }
    
    
    int size = sizeof(useful_stack_info)/ sizeof(int);
    //printf("SIZEOFTHING: %d\n",size);
    for (int i = 0; i <= 52; ++i){
        char buff[2048];
        fscanf(fp, "%s", buff);
        
      
        for( int j = 0; j < size; j ++){
            
            if(i == useful_stack_info[j]){
                if(i==52){
                   //printf("%d %s\n",i, buff);     
                   printf("%s\n", buff);     
                }
                //printf("%d: string: %s lu:%lu hex:%X 08X: %08X\n",i, buff, buff, buff, buff);
                else{
                    //printf("%d %08X\n",i, buff);
                    printf("%08X\n", buff);
                }
            }
        }
    }
    fclose(fp);
//  //cat /proc/{procnospace}/stat').read()   
}

// #include <stdio.h>
// int main(){
//     //int useful_stack_info[] = {23,26,27,28,29,30,45,46,47,48,49,50,51,52};
//     //char whatInfo[][]= {"vsize","startcode","endcode", "startStack", "currentESP", "currentEIP", "startData", "endData", "heapExpand", "argStart", "argEnd", "EnvStart", "EnvEnd", "ExitCode"};
    
// }