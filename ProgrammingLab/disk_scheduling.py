def look(requests, head_start, direction):
    sorted_arr = sorted(requests)

    sequences = []
    start_idx = 0
    while start_idx < len(sorted_arr) and sorted_arr[start_idx] < head_start:
        start_idx += 1

    if direction == "right":
        j = start_idx
        while j < len(sorted_arr):
            sequences.append(sorted_arr[j])
            j += 1

        j = start_idx - 1
        while j >= 0:
            sequences.append(sorted_arr[j])
            j -= 1
    else:
        j = start_idx - 1
        if head_start == sorted_arr[start_idx]:
            j = start_idx

        while j >= 0:
            sequences.append(sorted_arr[j])
            j -= 1

        j = start_idx
        if head_start == sorted_arr[start_idx]:
            j = start_idx + 1

        while j < len(sorted_arr):
            sequences.append(sorted_arr[j])
            j += 1

    print(sequences)

def cLook(requests, head_start, direction):
    sorted_arr = sorted(requests)

    sequences = []
    start_idx = 0
    while start_idx < len(sorted_arr) and sorted_arr[start_idx] < head_start:
        start_idx += 1

    if direction == "right":
        j = start_idx
        while j < len(sorted_arr):
            sequences.append(sorted_arr[j])
            j += 1

        j = 0
        while j < start_idx:
            sequences.append(sorted_arr[j])
            j += 1
    else:
        j = start_idx - 1
        if head_start == sorted_arr[start_idx]:
            j = start_idx
        while j >= 0:
            sequences.append(sorted_arr[j])
            j -= 1

        j = len(sorted_arr) - 1
        if head_start == sorted_arr[start_idx]:
            start_idx += 1
        while j >= start_idx:
            sequences.append(sorted_arr[j])
            j -= 1

    print(sequences)

def scan(requests, head_start, direction, track_no=200):
    sorted_arr = sorted(requests)

    sequences = []
    start_idx = 0
    while start_idx < len(sorted_arr) and sorted_arr[start_idx] < head_start:
        start_idx += 1

    if direction == "right":
        j = start_idx
        while j < len(sorted_arr):
            sequences.append(sorted_arr[j])
            j += 1

        if sorted_arr[-1] != track_no - 1:
            sequences.append(track_no - 1)
    
        j = start_idx - 1
        while j >= 0:
            sequences.append(sorted_arr[j])
            j -= 1
    else:
        j = start_idx - 1
        if head_start == sorted_arr[start_idx]:
            j = start_idx

        while j >= 0:
            sequences.append(sorted_arr[j])
            j -= 1

        if sorted_arr[0] != 0:
            sequences.append(0)

        j = start_idx
        if head_start == sorted_arr[start_idx]:
            j = start_idx + 1

        while j < len(sorted_arr):
            sequences.append(sorted_arr[j])
            j += 1

    print(sequences)

def main():
    requests = [176, 79, 34, 60, 92, 11, 41, 114]
    head_start = 60
    print("Look time : ")
    look(requests, head_start, "right")
    look(requests, head_start, "left")

    print("C-Look time : ")
    cLook(requests, head_start, "right")
    cLook(requests, head_start, "left")

    print("Scan time : ")
    scan(requests, head_start, "right")
    scan(requests, head_start, "left")

if __name__ == "__main__":
    main()