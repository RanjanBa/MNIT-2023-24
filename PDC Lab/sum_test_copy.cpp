#include <iostream>
#include <stdio.h>
#include <omp.h>

#define Arr_Size 1000000000

using namespace std;

int main(int argc, char const *argv[])
{
    double t1 = omp_get_wtime();

    long long sum = 0;

#pragma omp parallel
    {
        long long psum = 0;

#pragma omp for
        for (size_t i = 0; i < Arr_Size; i++)
        {
            psum++;
        }

#pragma omp critical
        cout << "psum : " << psum << "\n";
        sum += psum;
    }

    double t2 = omp_get_wtime();

    printf("Sum : %d , time: %f\n", sum, (t2 - t1));

    return 0;
}
