#include<iostream>
#include<omp.h>
#include<vector>

#define Mat_Size 1000

using namespace std;

vector<vector<int>> a(Mat_Size, vector<int>(Mat_Size));
vector<vector<int>> res(Mat_Size, vector<int>(Mat_Size));

void sequential() {
    for(int i = 0; i < Mat_Size; i++) {
        for(int j = 0; j < Mat_Size; j++) {
            res[i][j] = 0;
            for(int k = 0; k < Mat_Size; k++) {
                res[i][j] += a[i][k] * a[k][j];
            }
        }
    }
}

int doTask(int row, int col) {
    int sum_of_prod = 0;
    for(int i = 0; i < Mat_Size; i++) {
        sum_of_prod += a[row][i] * a[i][col];
    }

    return sum_of_prod;
}

void parallel() {
    #pragma omp parallel for
    for (size_t i = 0; i < Mat_Size; i++)
    {
        #pragma omp parallel for
        for (size_t j = 0; j < Mat_Size; j++)
        {
            res[i][j] = doTask(i, j);
        }
    }
}

int main(int argc, char const *argv[])
{
    for(int i = 0; i < Mat_Size; i++) {
        for (int j = 0; j < Mat_Size; j++)
        {
            a[i][j] = i * Mat_Size + j + 1;
        }
        
    }
    printf("Matrix Size : (%d X %d)\n", Mat_Size, Mat_Size);
    double t1, t2;
    t1 = omp_get_wtime();
    sequential();
    t2 = omp_get_wtime();
    printf("Sequential Multiplication Execution time : %f\n", (t2 - t1));
    t1 = omp_get_wtime();
    parallel();
    t2 = omp_get_wtime();
    printf("Parallel Multiplication Execution time : %f\n", (t2 - t1));
    return 0;
}
