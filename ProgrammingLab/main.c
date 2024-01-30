#include<stdio.h>
#include "functions.h"

int main() {
    while (-1)
    {
        printf("Enter:\n");
        printf("\t '1' to addition.\n");
        printf("\t '2' to subtract.\n");
        printf("\t '3' to multiply.\n");
        printf("\t '4' to division.\n");
        printf("\t 'Q' or 'q' to quit.\n");
        printf("Input character : ");
        char ch;
        scanf("%c", &ch);
        if(ch == 'Q' || ch == 'q') break;

        int a, b;
        printf("First integer : ");
        scanf("%d", &a);
        printf("Second integer : ");
        scanf("%d", &b);
        switch (ch)
        {
        case '1':
            printf("Additon of %d and %d is %d", a, b, add(a, b));
            break;
        case '2':
            printf("subtract of %d and %d is %d", a, b, subtract(a, b));
            break;
        case '3':
            printf("multiply of %d and %d is %d", a, b, multiply(a, b));
            break;
        case '4':
            printf("Division of %d and %d is %f", a, b, division(a, b));
            break;
        default:
            printf("%c is not valid input. Please enter valid character.", ch);
            break;
        }
        printf("\n\n");
    }
    return 0;
}