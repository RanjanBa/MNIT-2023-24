#include <stdio.h>
#include <math.h>
#include <mpi.h>
#define PI 3.1415926535
void parallel(int argc, char **argv, long long num_intervals)
{
    long long i = 0;
    int rank, num_procs, tag = 100;
    double rect_width, x_middle, area, sum;
    rect_width = PI / num_intervals;
    MPI_Init(&argc, &argv);
    double t1 = MPI_Wtime();
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &num_procs);
    int size_per_procs = num_intervals / num_procs;
    int start = rank * size_per_procs + 1;
    int end = (rank + 1) * size_per_procs;
    if (rank == 0)
    {
        sum = 0.0;
        for (int i = start; i <= end && i < num_intervals; i++)
        {
            x_middle = (i - 0.5) * rect_width;
            area = sin(x_middle) * rect_width;
            sum += area;
        }
        MPI_Status status; double p_sum = 0.0;
        for (int i = 1; i < num_procs; i++)
        {
            MPI_Recv(&p_sum, 1, MPI_DOUBLE, i, tag, MPI_COMM_WORLD, &status);
            sum += p_sum;
        }
        double t2 = MPI_Wtime();
        printf("The total area from Parallel Execution is : %f and time is : %f\n", (float)sum, (float)(t2 - t1));
    }
    else
    {
        double p_sum = 0.0; area = 0.0;
        for (int i = start; i <= end && i <= num_intervals; i++)
        {
            x_middle = (i - 0.5) * rect_width;
            area = sin(x_middle) * rect_width;
            p_sum += area;
        }
        MPI_Send(&p_sum, 1, MPI_DOUBLE, 0, tag, MPI_COMM_WORLD);
    }
    MPI_Finalize();
}
int main(int argc, char **argv)
{
    long long num_intervals = 10000;
    parallel(argc, argv, num_intervals);
    return 0;
}