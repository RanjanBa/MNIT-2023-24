#include <iostream>
#include <mpi.h>

using namespace std;

int main(int argc, char **argv)
{
    int rank, num_procs;
    int tag = 42;
    MPI_Status status;

    MPI_Init(&argc, &argv);

    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &num_procs);

    printf("I am %d of %d\n", rank, num_procs);

    int msg_count = 25;

    if (rank == 0)
    {
        char recv_msg[msg_count];
        MPI_Status status;
        for (int i = 1; i < num_procs; i++)
        {
            MPI_Recv(recv_msg, msg_count, MPI_CHAR, i, tag, MPI_COMM_WORLD, &status);
            printf("rank id %d : %s \n", i, recv_msg);
        }
    }
    else
    {
        char msg[msg_count] = {'H', 'e', 'l', 'l', 'o', ' ', 'F', 'r', 'o', 'm', ' ', char('0' + rank)};
        MPI_Send(msg, msg_count, MPI_CHAR, 0, tag, MPI_COMM_WORLD);
    }

    MPI_Finalize();

    return 0;
}
