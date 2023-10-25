#include<bits/stdc++.h>
#include<omp.h>

using namespace std;

int main(int argc, char const *argv[])
{
    int thread_id, threads_num;

    omp_set_num_threads(3);

    #pragma omp parallel private(thread_id) shared(threads_num)
    {
        thread_id = omp_get_thread_num();
        threads_num = omp_get_num_threads();

        printf("id : %d , total threads : %d\n", thread_id, threads_num);
    }

    return 0;
}
