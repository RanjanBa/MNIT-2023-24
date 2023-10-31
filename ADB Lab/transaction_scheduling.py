import sys

def permutations(visited, arr, result):
    if len(arr) == len(visited):
        print(arr)
        result.append(arr)
        return
    

    for i in range(len(visited)):
        if visited[i]:
            continue

        visited[i] = True
        arr.append(i+1)
        permutations(visited, arr, result)
        arr.remove(i+1)
        visited[i] = False
    
def main():
    file_name = ""

    if len(sys.argv) > 1:
        file_name = sys.argv[1]

    if len(file_name) == 0:
        file_name = "transactions.txt"

    file = open(file_name, "r")

    transactions = []
    original_transactions = []

    for l in file:
        if l[-1] == '\n':
            l = l[0:-1]
        print(l)
        words = l.split('|')

        if 'Transaction' in l or 'transaction' in l:
            continue

        for i, word in enumerate(words):
            word = word.strip()
            if i >= len(transactions):
                transactions.append([])
                original_transactions.append([])
            if(word != '---'):
                original_transactions[i].append(word)
            transactions[i].append(word)

    print(transactions)

    print(original_transactions)

    visited = [False] * 3
    arr = []
    result = []

    permutations(visited, arr, result)

    print(result)

    
    
if __name__ == "__main__":
    main()