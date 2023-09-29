#include<iostream>
#include<omp.h>
#include<vector>

#define Mat_Size 10000

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
    #pragma omp parallel
    #pragma omp for
    for (size_t i = 0; i < Mat_Size; i++)
    {
        for (size_t j = 0; j < Mat_Size; j++)
        {
            res[i][j] = doTask(i, j);
        }
    }
}

void showMat(vector<vector<int>> &vec) {
    for(int i = 0; i < Mat_Size; i++) {
        for(int j = 0; j < Mat_Size; j++) {
            printf("%d ", vec[i][j]);
        }

        printf("\n");
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

    printf("Original Mat : \n");
    showMat(a);

    // sequential();

    // printf("Sequential Multiplication Mat : \n");
    // showMat(res);


    parallel();
    
    printf("Parallel Multiplication Mat : \n");
    showMat(res);

    return 0;
}
