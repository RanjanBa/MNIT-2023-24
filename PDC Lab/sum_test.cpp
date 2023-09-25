#include<iostream>
#include<stdio.h>
#include<omp.h>

using namespace std;

int main(int argc, char const *argv[])
{
    long long mxN = 10000000000;
    long long sum = 0;
    int t_num = 0;

#pragma omp parallel
    t_num = omp_get_num_threads();

    long dis_size = mxN / t_num;

#pragma omp parallel
    {
        long long psum = 0;
        int t_id = omp_get_thread_num();

        for (size_t i = t_id * dis_size; i < t_id * dis_size + dis_size; i++)
        {
            psum++;
        }

#pragma omp critical
        cout << "psum : " << psum << "\n";
        sum += psum;
    }

    printf("Sum : %d\n", sum);

    return 0;
}
