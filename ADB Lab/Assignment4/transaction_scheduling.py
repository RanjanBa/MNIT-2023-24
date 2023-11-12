import sys

def permutations(visited, arr):
    if len(arr) == len(visited):
        return [[e for e in arr]]
    
    result = []

    for i in range(len(visited)):
        if visited[i]:
            continue

        visited[i] = True
        arr.append(i+1)
        res = permutations(visited, arr)
        arr.remove(i+1)
        visited[i] = False
        
        for r in res:
            result.append(r)
    
    return result

def isConfict(instruction1 : str, instruction2 : str):
    ins_typeA, attribA = instruction1.split('(')
    if attribA[-1] == ')':
        attribA = attribA[:-1]
    
    ins_typeB, attribB = instruction2.split('(')
    if attribB[-1] == ')':
        attribB = attribB[:-1]
        
    if attribA != attribB:
        return False
    
    if ins_typeA == 'R' and ins_typeB == 'R':
        return False
    
    return True
   
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

    # get all permutations
    visited = [False] * len(original_transactions)
    arr = []
    result = permutations(visited, arr)
    print(len(result))

    serial_transactions = []

    for res in result:
        serial = []
        
        for i in range(len(original_transactions)):
            trans = []
            for v in res:
                idx = v - 1
                
                if i == idx:
                    for ins in original_transactions[i]:
                        trans.append(ins)
                else:
                    for _ in original_transactions[i]:
                        trans.append('---')
            
            serial.append(trans)

        serial_transactions.append(serial)
    
    print('Serial Transactions : ')
    print(serial_transactions)
    
    print('Correct Positions : ')
    for serial in serial_transactions:
        is_confict = False
        for idx, transaction in enumerate(transactions):
            serial_pos = 0
            correct_positions = [-1] * len(transaction)
            for pos, ins in enumerate(transaction):
                if ins == '---':
                    continue
                
                while serial_pos < len(serial[idx]) and serial[idx][serial_pos] == '---':
                    serial_pos += 1

                if serial_pos == len(serial[idx]):
                    break
                
                if serial[idx][serial_pos] == ins:
                    correct_positions[pos] = serial_pos
                    serial_pos += 1
                
            print(serial[idx])
            print(transaction)
            print(correct_positions)
            print()
            
            for cur_pos, ori_pos in enumerate(correct_positions):
                if cur_pos == ori_pos or ori_pos == -1:
                    continue
                
                compare_list = []
                
                if cur_pos > pos:
                    compare_list = list(range(cur_pos - 1, ori_pos - 1, -1))
                else:
                    compare_list = list(range(cur_pos + 1, ori_pos + 1))
                
                for new_idx in range(len(transactions)):
                    if idx == new_idx:
                        continue
                    
                    for l in compare_list:
                        if transactions[new_idx][l] == '---':
                            continue

                        if isConfict(transactions[idx][cur_pos], transactions[new_idx][l]):
                            is_confict = True
                            break
                    
                    if is_confict:
                        break
                
                if is_confict:
                    break
        if not is_confict:
            print("Serializable")
        else:
            print("Not Serializable")
            
        print()

if __name__ == "__main__":
    main()