#include<stdio.h>
#include<pthread.h>
#include<errno.h>
#include<unistd.h>
#include<stdlib.h>
#include<string.h>

void* do_greeting(void* arg);

int main() {
    pthread_t thread1;
    int status;

    status = pthread_create(&thread1, NULL, do_greeting, NULL);

    sleep(2);

    if(status != 0) {
        fprintf(stderr, "thread create error %d: %s\n", status, strerror(status));
        exit(1);
    }

    return 0;
}

void* do_greeting(void* arg) {
    sleep(1);
    printf("Thread version of Hello, world.\n");

    return arg;
}