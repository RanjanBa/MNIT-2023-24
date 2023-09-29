#include<iostream>
#include<omp.h>

#define Arr_Size 10
#define Step_Size 1

using namespace std;

int a[Arr_Size];

int doSum(int start, int end) {
    int mid, x, y, res;

    if(start == end) {
        res = a[start];
    }
    else {
        mid = (start + end) / 2;
        printf("T_id : %d, Sum(%d, %d) = Sum(%d, %d) + Sum(%d, %d)\n", omp_get_thread_num(), start, end, start, mid, mid+1,end);

        #pragma omp task shared(x)
        x = doSum(start, mid);
        
        #pragma omp task shared(y)
        y = doSum(mid + 1, end);

        #pragma omp taskwait
        res = x + y;
    }

    printf("T_id: %d, Sum(%d, %d)=%d\n", omp_get_thread_num(), start, end, res);

    return res;
}

int main(int argc, char const *argv[])
{
    int i, sum = 0;

    for(int i =0; i < Arr_Size; i++) {
        a[i] = 1;
    }

    #pragma omp parallel
    #pragma omp single
    sum = doSum(0, Arr_Size - 1);

    return 0;
}
