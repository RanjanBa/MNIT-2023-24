#include<bits/stdc++.h>
#include<math.h>
#include<omp.h>

using namespace std;

int main(int argc, char const *argv[])
{
    long intervals;
    
    sscanf(argv[1], "%ld", &intervals);

    cout << "intervals : " << intervals << "\n";
    // cin >> intervals;

    double integral = 0.0;

    double dx = 1.0 / intervals;
    
    double t1 = omp_get_wtime();

    #pragma omp parrallel for reductions(+:integral)
    {
        for(int i = 0; i < intervals; i++) {
            double x = i * dx;
            double fx = sqrt(1.0 - x * x);
            integral = integral + fx * dx;
        }
    }

    double pi = 4 * integral;

    printf("%20.181f\n", pi);
    double t2 = omp_get_wtime();

    printf("Execution time : %fs", (t2 - t1));

    return 0;
}
