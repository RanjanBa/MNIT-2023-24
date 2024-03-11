from queue import PriorityQueue, Queue

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


def sortedArrivalTimes(table):
    arrival_times = []
        
    for i in range(len(table)):
        arrival_times.append((table[i][0], i))
    
    arrival_times.sort()
    print(arrival_times)

    return arrival_times


def fcfs(table):
    if len(table) == 0:
        return

    arrival_times = sortedArrivalTimes(table)

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
    if len(table) == 0:
        return

    arrival_times = sortedArrivalTimes(table)

    idx = 0
    ct = 0

    currently_available_processes = PriorityQueue()

    for i in range(len(table)):
        while idx < len(arrival_times) and arrival_times[idx][0] <= ct:
            currently_available_processes.put((table[arrival_times[idx][1]][1], arrival_times[idx][0], arrival_times[idx][1]))
            idx += 1

        if currently_available_processes.qsize() == 0 and idx < len(arrival_times) and arrival_times[idx][0] > ct:
            ct = arrival_times[idx][0]
            currently_available_processes.put((table[arrival_times[idx][1]][1], arrival_times[idx][0], arrival_times[idx][1]))

        val = currently_available_processes.get()
        table[val[2]][5] = ct - val[1]
        ct += val[0]
        table[val[2]][2] = ct


def srjf(table):
    if len(table) == 0:
        return
    
    arrival_times = sortedArrivalTimes(table)

    currently_available_processes = PriorityQueue()
    
    ct = arrival_times[0][0]

    visited_processes = set()

    for i in range(len(arrival_times)):
        while ct < arrival_times[i][0]:
            if currently_available_processes.qsize() == 0:
                ct = arrival_times[i][0]
                break
            
            execution_duration = arrival_times[i][0] - ct
            val = currently_available_processes.get()

            if not val[2] in visited_processes:
                print(f"First visited {val[2]} at {ct}")
                table[val[2]][5] = ct - val[1]
            visited_processes.add(val[2])

            if val[0] > execution_duration:
                print(f"Executing : {val[2]} : {val[0]}")
                remaining_time = val[0] - execution_duration
                currently_available_processes.put((remaining_time, val[1], val[2]))
                ct += execution_duration
            else:
                ct += val[0]
                table[val[2]][2] = ct

        currently_available_processes.put((table[arrival_times[i][1]][1], arrival_times[i][0], arrival_times[i][1]))
        execution_duration = 10000000
        if i < len(arrival_times) - 1:
            execution_duration = arrival_times[i+1][0] - arrival_times[i][0]

        val = currently_available_processes.get()      
 
        if not val[2] in visited_processes:
            # print(f"First visited {val[2]} at {ct}")
            table[val[2]][5] = ct - val[1]
        visited_processes.add(val[2])
 
        if val[0] > execution_duration:
            # print(f"Executing : {val[2]} : {execution_duration}")
            remaining_time = val[0] - execution_duration
            currently_available_processes.put((remaining_time, val[1], val[2]))
            ct += execution_duration
        else:
            # print(f"Executing : {val[2]} : {val[0]}")
            ct += val[0]
            table[val[2]][2] = ct
    
    while currently_available_processes.qsize() > 0:
        # print(f"Executing : {val[2]} : {val[0]}")
        val = currently_available_processes.get()

        if not val[2] in visited_processes:
            # print(f"First visited {val[2]} at {ct}")
            table[val[2]][5] = ct - val[1]
        visited_processes.add(val[2])

        ct += val[0]
        table[val[2]][2] = ct


def roundRobin(table):
    if len(table) == 0:
        return

    quantum_time = 2

    arrival_times = sortedArrivalTimes(table)

    currently_available_processes = Queue()
    ct = arrival_times[0][0]

    idx = 0
    
    visited_processes = set()

    while idx < len(arrival_times):
        while idx < len(arrival_times) and ct < arrival_times[idx][0]:
            if currently_available_processes.qsize() == 0:
                ct = arrival_times[idx][0]
                break
            
            # print(f"Current process : {val[0]}")
            val = currently_available_processes.get()
            
            if not val[0] in visited_processes:
                # print(f"First visited {val[0]} at {ct}")
                table[val[0]][5] = ct - table[val[0]][0]
            visited_processes.add(val[0])
            
            if val[1] > quantum_time:
                remaining_time = val[1] - quantum_time
                ct += quantum_time
                while idx < len(arrival_times) and ct >= arrival_times[idx][0]:
                    currently_available_processes.put((arrival_times[idx][1], table[arrival_times[idx][1]][1]))
                    idx += 1
                currently_available_processes.put((val[0], remaining_time))
            else:
                ct += val[1]
                table[val[0]][2] = ct

        while idx < len(arrival_times) and ct >= arrival_times[idx][0]:
            currently_available_processes.put((arrival_times[idx][1], table[arrival_times[idx][1]][1]))
            idx += 1
        
        val = currently_available_processes.get()
        
        if not val[0] in visited_processes:
            # print(f"First visited {val[0]} at {ct}")
            table[val[0]][5] = ct - table[val[0]][0]
        visited_processes.add(val[0])
        
        # print(f"Current process : {val[0]}")
        
        if val[1] > quantum_time:
            remaining_time = val[1] - quantum_time
            ct += quantum_time
            while idx < len(arrival_times) and ct >= arrival_times[idx][0]:
                currently_available_processes.put((arrival_times[idx][1], table[arrival_times[idx][1]][1]))
                idx += 1
            currently_available_processes.put((val[0], remaining_time))
        else:
            ct += val[1]
            table[val[0]][2] = ct
        
        # print(f"Completion time : {ct}")
        
    while currently_available_processes.qsize():
        # print(f"Current process : {val[0]}")
        val = currently_available_processes.get()
        if not val[0] in visited_processes:
            # print(f"First visited {val[0]} at {ct}")
            table[val[0]][5] = ct - table[val[0]][0]
        visited_processes.add(val[0])

        if val[1] > quantum_time:
            remaining_time = val[1] - quantum_time
            currently_available_processes.put((val[0], remaining_time))
            ct += quantum_time
        else:
            ct += val[1]
            table[val[0]][2] = ct
        
        # print(f"Completion time : {ct}")

def copyTable(table):
    n = len(table)
    m = len(table[0])
    print(n)
    new_table = [[0 for i in range(m)] for _ in range(n)]
    
    for i in range(n):
        for j in range(m):
            new_table[i][j] = table[i][j]

    return new_table

def calculateTAT(table):
    n = len(table)
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
    
    # Calculate Average Total turn around time
    total_turn_around = 0
    for i in range(n):
        total_turn_around += table[i][3]
    
    avg_turn = total_turn_around / n
    print(f"Total waiting time : {total_turn_around}")
    print(f"Average waiting time : {avg_turn}")

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
    
    new_table = copyTable(table)
    fcfs(new_table)
    calculateTAT(new_table)
    print()

    new_table = copyTable(table)
    sjf(new_table)
    calculateTAT(new_table)
    print()
    
    new_table = copyTable(table)
    srjf(new_table)
    calculateTAT(new_table)
    print()
    
    new_table = copyTable(table)
    roundRobin(new_table)
    calculateTAT(new_table)
    print()

        
if __name__ == "__main__":
    main()
