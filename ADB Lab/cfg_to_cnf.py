def show_grammar(grammar : dict[str, list]):
    for k in grammar:
        if k == "S0":
            print(k, "->", "|".join(grammar[k]))

    for k in grammar:
        if k != "S0":
            print(k, "->", "|".join(grammar[k]))

def main():
    file = open("cfg_grammar.txt", "r")

    grammar = {}

    for l in file:
        l = l[:-1]
        print(l)
        rule = l.split("->")

        w = ""
        
        words = []

        for i in range(len(rule[1])):
            if rule[1][i] == " ":
                continue

            if rule[1][i] == "|":
                words.append(w)
                w = ""
                continue

            w += rule[1][i]

        if w != "":
            words.append(w)

        grammar[rule[0].strip()] = words

    # Eliminate start symbol from RHS

    for k in grammar:
        words = grammar[k]
        found = False
        for w in words:
            idx = w.find("S")

            if idx + 1 < len(w):
                grammar["S0"] = [k]
                found = True
                break

        if found:
            break

    show_grammar(grammar)

    # Eliminate null productions
    
    null_production_keys = []

    while True:
        null_production_keys = []
        for k in grammar:
            words = grammar[k]

            for w in words:
                if w == "ε":
                    null_production_keys.append(k)
                    words.remove(w)
                    break
        
        if len(null_production_keys) == 0:
            break
        
        for k in grammar:
            words = grammar[k]

            for idx in range(len(words)):
                for p in null_production_keys:
                    words[idx].replace(p, "")
        
    
    show_grammar(grammar)


if __name__ == "__main__":
    main()
