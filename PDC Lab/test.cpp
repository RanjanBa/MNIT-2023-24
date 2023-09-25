#include <stdio.h>
#include <omp.h>

using namespace std;

int main(int argc, char const *argv[])
{
    int t_id, t_num;

#pragma omp parallel private(t_id)
    {
        t_id = omp_get_thread_num();
        t_num = omp_get_num_threads();

        printf("id : %d, total threads : %d\n", t_id, t_num);
    }

    return 0;
}
