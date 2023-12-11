#include<iostream>
#include "mpi.h"

using namespace std;

int main(int argc, char **argv)
{
    int rank, num_procs;

    MPI_Init(&argc, &argv);

    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &num_procs);

    printf("Hello World. I am %d of %d\n", rank, num_procs);

    MPI_Finalize();

    return 0;
}
