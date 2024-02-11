#include "functions.h"
#include <math.h>

int toDecimal(int base, int num) {
    int sign = 1;
    if(num < 0) {
        sign = -1;
    }
    
    num = abs(num);
    
    int ans = 0;
    int p = 1;
    while (num > 0)
    {
        int r = num % 10;
        ans += r * p;
        p *= base;
        num /= 10;
    }
    
    return ans * sign;
}

int fromDecimalToDifferentBase(int base, int decimal) {
    int ans = 0;
    int p = 1;

    while (decimal > 0)
    {
        int r = decimal % base;
        r *= p;
        ans += r;
        p *= 10;
        decimal /= base;
    }
    
    return ans;
}