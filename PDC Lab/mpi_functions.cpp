#include<iostream>
#include<mpi.h>

using namespace std;

int main(int argc, char **argv)
{
    int rank, size;
    int msg[2] = {10, 20};
    int tag = 42;
    MPI_Status status;

    MPI_Init(&argc, &argv);

    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    if(rank == 0) {
        MPI_Send(msg, 2, MPI_INT, 1, tag,  MPI_COMM_WORLD);
    } else if(rank == size - 1) {
        MPI_Recv(msg, 2, MPI_INT, rank-1, tag, MPI_COMM_WORLD, &status);
    } else {
        MPI_Recv(msg, 2, MPI_INT, rank-1, tag, MPI_COMM_WORLD, &status);
        MPI_Send(msg, 2, MPI_INT, rank+1, tag,  MPI_COMM_WORLD);
    }

   printf("I am %d of %d with msg %d\n", rank, size, msg[0]);

    MPI_Finalize();

    return 0;
}
