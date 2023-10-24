#include<stdio.h>
#include<iostream>
#include<errno.h>
#include<unistd.h>
#include<stdlib.h>
#include<string.h>

using namespace std;

void* do_greeting2(void* arg);

int main() {
    pthread_t thread1, thread2;

    void *result1, *result2;

    int status;

    if((status = pthread_create(&thread1, NULL, do_greeting2, NULL)) != 0) {
        cerr << "thread create error: " << strerror(status) << endl;
        exit(1);
    }

    if((status = pthread_create(&thread2, NULL, do_greeting2, NULL)) != 0) {
        cerr << "thread create error: " << strerror(status) << endl;
        exit(1);
    }

    if((status = pthread_join(thread1, &result1)) != 0) {
        cerr << "join error: " << strerror(status) << endl;
        exit(1);
    }

    if((status = pthread_join(thread2, &result2)) != 0) {
        cerr << "join error: " << strerror(status) << endl;
        exit(1);
    }

    if(result1 != NULL || result2 != NULL) {
        cerr << "bad result" << endl;
        exit(1);
    }

    return 0;
}

void* do_greeting2(void* arg) {
    int val = rand() % 2;

    for(int loop = 0; loop < 10; loop++) {
        sleep(1);
        if(!val) cout << "Hello ";
        else cout << "World\n";
    }

    return arg;
}