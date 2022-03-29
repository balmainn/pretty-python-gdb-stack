#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#define PI 3.14159265
float f(float x, float y){
    double b = x*y;
    float output = x-y;
    return output;
}

int main(){
    

    float x = .75;
    float y = 0.2;
    float maxVal = 1;
    int steps = 8;
    float h = 0.5;
    float function = f(x,y);
    printf("n       x        y\n");
    int ctr = 0;
    printf("%d  %f   %f \n",ctr, x, y);
    for (float i = x; i < maxVal; i+=h ){
        y = y+h*function;
        x = x+h;
        ctr ++;
        function = f(x,y);
        printf("%d  %f   %f \n",ctr, x, y);
    }
  
}
