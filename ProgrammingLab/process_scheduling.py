from queue import PriorityQueue

table_ids = ['ID', 'AT', 'BT', 'CT', 'TAT', 'WT', 'RT']

def showTable(table):
    for i in range(len(table_ids)):
        print(table_ids[i], end="\t")
    print()
    for i in range(len(table)):
        print(i, end="\t")
        for j in range(len(table[i])):
                print(table[i][j], end="\t")
        print()


def fcfs(table):
    arrival_times = []
    for i in range(len(table)):
        arrival_times.append((table[i][0], i))

    arrival_times.sort()

    print(arrival_times)

    ct = 0

    for i in range(len(arrival_times)):
        if ct >= arrival_times[i][0]:
            table[arrival_times[i][1]][5] = ct - arrival_times[i][0]
            ct += table[arrival_times[i][1]][1]
        else:
            ct = arrival_times[i][0] + table[arrival_times[i][1]][1]
            table[arrival_times[i][1]][5] = 0
        table[arrival_times[i][1]][2] = ct


def sjf(table):
    arrival_times = []
    for i in range(len(table)):
        arrival_times.append((table[i][0], i))

    arrival_times.sort()
    print(arrival_times)

    idx = 0
    ct = 0

    current_available_processes = PriorityQueue()

    for i in range(len(table)):
        while idx < len(arrival_times) and arrival_times[idx][0] <= ct:
            currently_available_processes.put((table[arrival_times[idx][1]][1], arrival_times[idx][0], arrival_times[idx][1]))
            idx += 1

        if len(currently_available_processes) == 0 and idx < len(arrival_times) and arrival_times[idx][0] > ct:
            ct = arrival_times[idx][0]
            currently_available_processes.put((table[arrival_times[idx][1]][1], arrival_times[idx][0], arrival_times[idx][1]))

        val = currently_available_processes.get()
        print(val)
        ct += val[0]
        table[val[2]][2] = ct

def main():
    n = int(input("How many process are there ? "))
    print()
    table = [[0 for j in range(6)] for _ in range(n)]
    for i in range(n):
        at = int(input(f"Arrival time of process{i} : ")) 
        bt = int(input(f"Burst time of process{i} : "))
        table[i][0] = at
        table[i][1] = bt
        print()

    # fcfs(table)

    sjf(table)

    for i in range(n):
        table[i][3] = table[i][2] - table[i][0]
        table[i][4] = table[i][3] - table[i][1]

    print()
    showTable(table)

    # Calculate Average waiting time
    total_wait = 0
    for i in range(n):
        total_wait += table[i][4]
    
    avg_wt = total_wait / n
    print(f"Total waiting time : {total_wait}")
    print(f"Average waiting time : {avg_wt}")
        
if __name__ == "__main__":
    main()
