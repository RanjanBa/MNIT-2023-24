# epsilon : \u03B5
# lamda : \u03BB


def showGrammar(grammar : dict[str, set[str]]):
    for k in grammar:
        if k == "S0":
            print(k, "->", "|".join(grammar[k]))

    for k in grammar:
        if k != "S0":
            print(k, "->", "|".join(grammar[k]))

def findPossibleWords(word : str, idx : int, key : str, possible_words : set[str]):
    if len(word) == 0:
        return

    if idx >= len(word):
        return
    
    for i in range(idx, len(word)):
        if word[i] == key:
            if len(word) == 1:
                possible_words.add("null")
                continue

            new_word = word[0:i] + word[i+1:]

            possible_words.add(new_word)
            
            findPossibleWords(new_word, i, key, possible_words)
            findPossibleWords(word, i + 1, key, possible_words)

def convertCfgToCnf(grammar : dict[str, set[str]]):
    # Eliminate start symbol from RHS

    print("\nEliminating Start Symbol :")

    words = grammar['S']

    for w in words:
        idx = w.find("S")

        if idx != -1:
            grammar["S0"] = set()
            grammar["S0"].add('S')
            break

    showGrammar(grammar)

    print("\nRemoving self loop : ")
    
    
    # for removing self loop
    for k in grammar:
        li = list(grammar[k])
        for j in range(len(li) - 1, -1, -1):
            if k == li[j]:
                grammar[k].pop(k)

    showGrammar(grammar)

    # Eliminate null productions
    
    print("\nRemoving Epsilon : ")

    used_null_production_keys = set()

    while True:
        null_production_keys = []
        for k in grammar:
            words = grammar[k]

            for w in words:
                if w == "null":
                    words.remove(w)
                    if not k in used_null_production_keys:
                        null_production_keys.append(k)
                        used_null_production_keys.add(k)

                    break
        
        if len(null_production_keys) == 0:
            break
        
        for k in grammar:
            words = list(grammar[k])

            for idx in range(len(words)):
                for p in null_production_keys:
                    # if words[idx].find(p) >= 0:
                    #     w = words[idx].replace(p, "")
                    #     if len(w) == 0:
                    #         w = "null"
                    #     words.append(w)
                    possible_words = set()
                    findPossibleWords(words[idx], 0, p, possible_words)
                    
                    for w in possible_words:
                        grammar[k].add(w)

        showGrammar(grammar)
        print()
    
    # Eliminate unit productions
    print("Removing unit productions :")
    while True:
        unit_productions = []

        for k in grammar:
            words = list(grammar[k])
            for w in words:
                if len(w) == 1 and w.isupper():
                    unit_productions.append((k, w))
                    grammar[k].remove(w)

        if len(unit_productions) == 0:
            break

        for p in unit_productions:
            if len(grammar[p[0]]) == 0:
                for w2 in grammar[p[1]]:
                    grammar[p[0]].add(w2)
            else:
                for w2 in grammar[p[1]]:
                    found = False
                    words = list(grammar[p[0]])
                    for j in range(len(words)):
                        w1 = words[j]

                        if w2 == w1:
                            found = True
                            break
                    
                    if not found:
                        grammar[p[0]].add(w2)

        showGrammar(grammar)
        print()

    # Eliminate useless productions

    print("Removing useless productions :")

    variables = set()

    for k in grammar:
        variables.add(k)
        for word in grammar[k]:
            for ch in word:
                if ch.isupper():
                    variables.add(ch)

    print(variables)

    visited_var = {}
    for v in variables:
        visited_var[v] = False

    root = 'S'
    if grammar.__contains__('S0'):
        root = 'S0'

    parents = []

    parents.append(root)

    while len(parents) > 0:
        children = []

        while len(parents) > 0:
            p = parents.pop(0)

            visited_var[p] = True

            for word in grammar[p]:
                for ch in word:
                    if ch.isupper() and visited_var[ch] == False:
                        children.append(ch)

        parents = children

    print(visited_var)

    for k in visited_var:
        if visited_var[k] == False and k in grammar.keys():
            grammar.pop(k)

    showGrammar(grammar)

    # Eliminate terminals from RHS if they exist with other terminals or non-terminals.
    
    print("\nEliminate terminals from RHS if they exist with other terminals or non-terminals : ")
    
    availables_var = []
    
    for i in range(26):
        ch = chr(ord('A') + i)
        found = False
        for v in variables:
            if ch == v:
                found = True
                break
            
        if not found:
            availables_var.append(ch)

    new_variables = {}
    
    for k in grammar:
        words = list(grammar[k])
        for i in range(len(words)):
            if len(words[i]) > 1 and  not words[i].isupper():
                for ch in words[i]:
                    if ch.islower():
                        if not ch in new_variables.keys():
                            new_variables[ch] = availables_var.pop(0)

                        new_word = words[i].replace(ch,new_variables[ch])
                        if words[i] in grammar[k]:
                            grammar[k].remove(words[i])
                        grammar[k].add(new_word)

    for ch in new_variables:
        grammar[new_variables[ch]] = set(ch)
        
    showGrammar(grammar)
    
    print("\nEliminate RHS with more than two non-terminals :")
    
    new_variables = {}
    
    while True:
        for k in grammar:
            words = list(grammar[k])
            for i in range(len(words)):
                if len(words[i]) > 2 and words[i].isupper():
                    found = False
                    word = words[i]
                    word_key = word[:2]
                    
                    for new_var in new_variables:
                        if word.find(new_var) != -1:
                            found = True
                            word_key = new_var
                            break
                    
                    if not found:
                        new_variables[word[:2]] = availables_var.pop(0)
                    
                    new_word = word.replace(word_key, new_variables[word_key])
                    
                    if word in grammar[k]:
                        grammar[k].remove(word)
                    
                    grammar[k].add(new_word)
                    
        can_break = True
        
        for k in grammar:
            for word in grammar[k]:
                if len(word) > 2:
                    can_break = False
                    break
        
            if not can_break:
                break
                
        if can_break:
            break

    for ch in new_variables:
        grammar[new_variables[ch]] = [ch]

    showGrammar(grammar)

    print("\nFinal CNF : ")
    showGrammar(grammar)

def main():
    file = open("cfg_grammar.txt", "r")

    grammar : dict[str, set[str]] = {}

    for l in file:
        if l[-1] == "\n":
            l = l[:-1]
        print(l)
        rule = l.split("->")

        w = ""
        
        words = set()

        for i in range(len(rule[1])):
            if rule[1][i] == " ":
                continue

            if rule[1][i] == "|":
                words.add(w)
                w = ""
                continue

            w += rule[1][i]

        if w != "":
            words.add(w)

        grammar[rule[0].strip()] = words

    convertCfgToCnf(grammar)
    
    # possible_words = set()
    # findPossibleWords("AA", 0, 'A', possible_words)
    # print(possible_words)

if __name__ == "__main__":
    main()
