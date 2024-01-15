import re

KEYWORDS = ['int', 'string', 'printf', 'scanf']
OPERATORS = ['-', '+', '*', '/', '=', '++', '--', '+=', '-=', '*=', '/=']

class Token:
    def __init__(self, key : str, line : int, start : int) -> None:
        self.key = key
        self.line_number = line
        self.start_index = start

    def __str__(self) -> str:
        return f"({self.key}, {self.line_number}, {self.start_index})"

list_keywords = []
list_identifiers = []
list_operators = []

def main():
    file = open('input.txt', 'r')
    for line_idx, line in enumerate(file):
        if line == "\n":
            break
        
        line_length = len(line)
        ch_idx = 0
        while ch_idx < line_length:
            found = False
            if ch_idx == 0 or (ch_idx > 0 and line[ch_idx-1] in [' ', '+', '-', '*', '/']):
                for k_w in KEYWORDS:
                    last_ch_idx = ch_idx + len(k_w)
                    word = line[ch_idx : last_ch_idx]
                    if word == k_w and (last_ch_idx >= line_length or line[last_ch_idx] in [' ', '(', '\n'] or line[last_ch_idx] in OPERATORS):
                        list_keywords.append(Token(word, line_idx, ch_idx))
                        ch_idx = last_ch_idx
                        found = True
                        break

            if not found:
                for o_w in reversed(OPERATORS):
                    last_ch_idx = ch_idx + len(o_w)
                    word = line[ch_idx : last_ch_idx]
                    if word == o_w:
                        list_operators.append(Token(word, line_idx, ch_idx))
                        ch_idx = last_ch_idx
                        found = True
                        break
            
            if not found:
                cur_idx = ch_idx
                new_word = ""
                while cur_idx < line_length and not line[cur_idx] in [' ', '\n', '(', ')'] and not line[cur_idx] in OPERATORS:
                    new_word += line[cur_idx]
                    cur_idx += 1

                list_identifiers.append(Token(new_word, line_idx, ch_idx))
                ch_idx = cur_idx

            ch_idx += 1

    for k in list_keywords:
        print(k)
    
    for k in list_operators:
        print(k)

    for k in list_identifiers:
        print(k)

if __name__ == "__main__":
    main()