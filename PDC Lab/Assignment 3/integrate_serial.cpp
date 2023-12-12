#include <stdio.h>
#include <math.h>
#include <chrono>
#include <ctime> 

#define PI 3.1415926535

double serial(long long num_intervals)
{
    long long i;
    double rect_width, area, sum, x_middle;

    rect_width = PI / num_intervals;
    sum = 0;
    for (i = 1; i < num_intervals + 1; i++)
    {
        /* find the middle of the interval on the X-axis. */
        x_middle = (i - 0.5) * rect_width;
        area = sin(x_middle) * rect_width;
        sum = sum + area;
    }
    
    return sum;
}

int main(int argc, char **argv)
{
    long long num_intervals;

    num_intervals = 10000000;

    auto start = std::chrono::system_clock::now();
    
    double sum = serial(num_intervals);

    auto end = std::chrono::system_clock::now();

    std::chrono::duration<double> elapsed_seconds = end-start;

    printf("The total area from Serial Execution is : %f and time is : %f\n", (float)sum, (float)elapsed_seconds.count());

    return 0;
}