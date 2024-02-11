#include <stdio.h>
#include <stdlib.h>
#include "functions.h"

char req_chs[6] = {'1', '2', '3', '4', '5', '6'};

int main()
{
    while (-1)
    {
        printf("Enter:\n");
        printf("\t '1' to addition.\n");
        printf("\t '2' to subtract.\n");
        printf("\t '3' to multiply.\n");
        printf("\t '4' to division.\n");
        printf("\t '5' to change to decimal\n");
        printf("\t '6' to change to different base\n");
        printf("\t 'Q' or 'q' to quit.\n");
        printf("Input character : ");
        char ch;
        scanf("%c", &ch);
        if (ch == 'Q' || ch == 'q')
            break;
        int is_req_char = 0;
        for (int i = 0; i < 6; i++)
        {
            if (ch == req_chs[i])
            {
                is_req_char = 1;
                break;
            }
        }
        if (is_req_char == 0)
        {
            printf("Valid Input is not given.\n");
            continue;
        }
        fflush(stdin);
        int a, b;
        printf("First integer : ");
        scanf("%d", &a);
        printf("Second integer : ");
        scanf("%d", &b);
        fflush(stdin);
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
        case '5':
            if(a < 2) {
                printf("Not valid base %d", a);
                break;
            }
            printf("Decimal Conversion from %d with base %d to %d", a, b, toDecimal(a, b));
            break;
        case '6':
            if(a < 2) {
                printf("Not valid base %d", a);
                break;
            }
            printf("Conversion of %d to base %d is %d", b, a, fromDecimalToDifferentBase(a, b));
            break;
        default:
            printf("%c is not valid input. Please enter valid character.", ch);
            break;
        }
        printf("\n\n");
    }
    return 0;
}