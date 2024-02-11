#include<stdio.h>
#include "functions.h"

float division(int a, int b) {
    if(b == 0) {
        printf("Can't divide with %d", b);
        return 0;
    }

    return (float) a / b;
}