VAR_KEYWORDS = ['int', 'string']
FUNC_KEYWORDS = ['printf', 'scanf']
OPERATORS = ['-', '+', '*', '/', '=']

list_variables = {}
variables_with_value = {}

def checkValue(val : str, typ : str):
    if len(val) == 0:
        return None
    
    if val[-1] == '\n' or val[-1] == ';':
        if len(val) == 1:
            return None
        val = val[:-1]
    
    if typ == VAR_KEYWORDS[0]:
        if val.isdigit():
            return int(val)
    elif typ == VAR_KEYWORDS[1]:
        if val[0] == '"' and val[-1] == '"':
            val = val[1:-1]
            return val
    
    return None

def splitPrintf(statement: str, line_no : int):
    words = statement.split(',')
    
    variables = []
    
    for idx in range(1, len(words)):
        w = words[idx].strip()
        variables.append(w)
        
    # print(variables)

    print_statement = words[0].strip()
    
    result_printf = ""
    
    var_index = 0
    
    if print_statement[0] == '"' and print_statement[-1] == '"' and len(print_statement) > 2:
        print_statement = print_statement[1:-1]
        print(print_statement)
        idx = 0
        while idx  < len(print_statement) - 1:
            if print_statement[idx] == "%":
                if print_statement[idx + 1] == "d" and (idx + 2 >= len(print_statement) or print_statement[idx + 2] == ' '):
                    if var_index >= len(variables):
                        print(f"Number of input is not equal in line {line_no}")
                        return False
                    var_name = variables[var_index]
                    if var_name in list_variables:
                        if list_variables[var_name] == 'int':
                            result_printf += str(variables_with_value[var_name])
                            var_index += 1
                            idx += 1
                        else:
                            print(f"Can't cast variable {var_name} from string to int in line {line_no}")
                            return False
                    else:
                        print(f"Variable {var_name} is not defined in line {line_no}")
                        return False
                elif print_statement[idx + 1] == "s" and (idx + 2 >= len(print_statement) or print_statement[idx + 2] == ' '):
                    if var_index >= len(variables):
                        print(f"Number of input is not equal in line {line_no}")
                        return False
                    var_name = variables[var_index]
                    if var_name in list_variables:
                        if list_variables[var_name] == 'string':
                            result_printf += str(variables_with_value[var_name])
                            var_index += 1
                            idx += 1
                        else:
                            print(f"Can't cast variable {var_name} from int to string in line {line_no}")
                            return False
                    else:
                        print(f"Variable {var_name} is not defined in line {line_no}")
                        return False
            else:
                result_printf += print_statement[idx]
            idx += 1
    else:
        print(f"Printf statement format isn't correct in line {line_no}")
        return False
    
    while var_index < len(variables):
        if not variables[var_index] in list_variables:
            print(f"Variable {variables[var_index]} is not defined in line {line_no}")
            return False
        
        var_index += 1
        
    print(result_printf)
    return True

def splitScanf(statement : str, line_no : int):
    words = statement.split(',')
    # print(words)
    
    for idx in range(len(words)):
        w = words[idx].strip()
        
        if idx == 0:
            if w[0] != '"' or w[-1] != '"':
                print(f"Printf statement format isn't correct in line {line_no}")
                return False
        else:
            if w[0] == '&':
                w = w[1:]
            
            if not w in list_variables:
                print(f"Variable {w} is not defined in line {line_no}")
                return False
            
    return True

def check(line : str, line_no : int) -> bool:
    line_length = len(line)
    ch_idx = 0
    
    while ch_idx < line_length and line[ch_idx] == ' ':
        ch_idx += 1
    
    if ch_idx >= line_length:
        return True
    
    for k in VAR_KEYWORDS:
        last_idx = ch_idx + len(k)
        w = line[ch_idx:last_idx]
        if w == k and (last_idx >= line_length or line[last_idx] in [' ', '\n', '('] or line[last_idx] in OPERATORS):
            ch_idx = last_idx + 1
            
            while ch_idx < line_length and line[ch_idx] == ' ':
                ch_idx += 1
            
            if ch_idx >= line_length:
                print(f"No variable name is found in line {line_no}")
                return False
            else:                
                var_name = ""
                
                if line[ch_idx].isdigit():
                    print(f"variable name can't start with digit in line {line_no}")
                    return False
                
                while ch_idx < line_length and (line[ch_idx].isalpha() or line[ch_idx] == '_'):
                    var_name += line[ch_idx]
                    ch_idx += 1
                
                if var_name == "":
                    print(f"No variable found in line {line_no}")
                    return False

                if var_name in list_variables:
                    print(f"Variable {var_name} is already defined in line {line_no}")
                    return False
                
                list_variables[var_name] = k
                if k == 'int':
                    variables_with_value[var_name] = 0
                elif k == 'string':
                    variables_with_value[var_name] = ""
                
                if ch_idx >= line_length:
                    # print(f"No equal(=) sign detected in line {line_no}")
                    return True
                
                while ch_idx < line_length and line[ch_idx] == ' ':
                    ch_idx += 1
                    
                if ch_idx < line_length and line[ch_idx] == '=':
                    ch_idx = ch_idx + 1
                    while ch_idx < line_length and line[ch_idx] == ' ':
                        ch_idx += 1
                        
                    if ch_idx >= line_length:
                        print(f"Can't assign anything in line {line_no}")
                    
                    val = ""
                    while ch_idx < line_length:
                        if line[ch_idx] != '\n':
                            val += line[ch_idx]
                        ch_idx += 1
                    
                    cast_val = checkValue(val, k)
                    
                    if cast_val == None:
                        print(f"Can't assign value : {val} to the variable in line {line_no}")
                        return False
                    
                    variables_with_value[var_name] = cast_val
                    return True
                else:
                    # print(f"No equal(=) sign detected in line {line_no}")
                    return True

    for k in FUNC_KEYWORDS:
        last_idx = ch_idx + len(k)
        w = line[ch_idx:last_idx]
        if w == k and (last_idx >= line_length or line[last_idx] in [' ', '(']):
            ch_idx = last_idx
            while ch_idx < line_length and line[ch_idx] == ' ':
                ch_idx += 1
            
            last_bracket_idx = line_length - 1
            
            while last_bracket_idx >= 0 and line[last_bracket_idx] in [' ', ';', '\n']:
                last_bracket_idx -= 1
                
            if line[last_bracket_idx] != ')' or ch_idx + 1 >= last_bracket_idx:
                print(f"Syntex is not correct in line {line_no}")
                return False
            
            statement = line[ch_idx + 1:last_bracket_idx]
            if k == "printf":
                return splitPrintf(statement, line_no)
            elif k == "scanf":
                return splitScanf(statement, line_no)

            return True

    var_name1 = ""
    
    while ch_idx < line_length and not line[ch_idx] in [' ', '\n', '(', ')']:
        var_name1 += line[ch_idx]
        ch_idx += 1
    
    while ch_idx < line_length and line[ch_idx] == ' ':
        ch_idx += 1
    
    if ch_idx >= line_length:
        print(f"Not equal (=) sign is found in line {line_no}")
        return False
    
    var_name2 = ""
    operator = None
    
    if line[ch_idx] == '+':
        ch_idx += 1
        if line[ch_idx] == '=':
            ch_idx += 1
            var_name2 = var_name1
            operator = '+'
        else:
            print(f"Syntex is not correct in line {line_no}")
            return False
    elif line[ch_idx] == '-':
        ch_idx += 1
        if line[ch_idx] == '=':
            ch_idx += 1
            var_name2 = var_name1
            operator = '-'
        else:
            print(f"Syntex is not correct in line {line_no}")
            return False
    elif line[ch_idx] == '*':
        ch_idx += 1
        if line[ch_idx] == '=':
            ch_idx += 1
            var_name2 = var_name1
            operator = '*'
        else:
            print(f"Syntex is not correct in line {line_no}")
            return False
    elif line[ch_idx] == '/':
        ch_idx += 1
        if line[ch_idx] == '=':
            ch_idx += 1
            var_name2 = var_name1
            operator = '/'
        else:
            print(f"Syntex is not correct in line {line_no}")
            return False
    elif  line[ch_idx] == '=':
        ch_idx += 1
        
        while ch_idx < line_length and line[ch_idx] == ' ':
            ch_idx += 1
    
        if ch_idx >= line_length:
            print(f"Syntex is not correct in line {line_no}")
            return False
        
        while ch_idx < line_length and not line[ch_idx] in [' ', '\n', '(', ')']:
            var_name2 += line[ch_idx]
            ch_idx += 1
            
        while ch_idx < line_length and line[ch_idx] == ' ':
            ch_idx += 1
            
        if ch_idx >= line_length:
            print(f"Syntex is not correct in line {line_no}")
            return False
        
        if line[ch_idx] in OPERATORS:
            operator = line[ch_idx]
            ch_idx += 1
    
    while ch_idx < line_length and line[ch_idx] == ' ':
        ch_idx += 1
        
    if ch_idx >= line_length:
        print(f"Syntex is not correct in line {line_no}")
        return False
    
    var_name3 = ""
    while ch_idx < line_length and not line[ch_idx] in [' ', '\n', '(', ')']:
        var_name3 += line[ch_idx]
        ch_idx += 1
    
    if not var_name1 in list_variables:
        print(f"{var_name1} is not defined in line {line_no}")
        return False
    
    val2 = None
    if not var_name2 in list_variables:
        val2 = checkValue(var_name2, list_variables[var_name1])
        if val2 == None:
            print(f"{var_name2} can't be cast to {list_variables[var_name1]} in line {line_no}")
            return False
    else:
        if list_variables[var_name1] == list_variables[var_name2]:
            val2 = variables_with_value[var_name2]
        else:
            print(f"can't cast type from {list_variables[var_name2]} to {list_variables[var_name1]} in line {line_no}")
            return False
    
    val3 = None
    if not var_name3 in list_variables:
        val3 = checkValue(var_name3, list_variables[var_name1])
        if val3 == None:
            print(f"{var_name3} can't be cast to {list_variables[var_name1]} in line {line_no}")
            return False
    else:
        if list_variables[var_name1] == list_variables[var_name3]:
            val3 = variables_with_value[var_name3]
        else:
            print(f"can't cast type from {list_variables[var_name3]} to {list_variables[var_name1]} in line {line_no}")
            return False
    
    val = None
    if operator == '+': 
        val = val2 + val3
    elif operator == '-':
       if list_variables[var_name1] == 'int':
           val = val2 - val3
       else:
           print(f"Two string can't be subtracted in line {line_no}")
           return False
    elif operator == '*':
        if list_variables[var_name1] == 'int':
           val = val2 * val3
        else:
            print(f"Two string can't be multiplied in line {line_no}")
            return False
    elif operator == '/':
        if list_variables[var_name1] == 'int':
           val = val2 // val3
        else:
            print(f"Two string can't be divided in line {line_no}")
            return False
    else:
        print(f"Operator {operator} is not defined in line {line_no}")
        return False
    
    variables_with_value[var_name1] = val
    
    return True
    
def main():
    file = open('input.txt', 'r')
    for line_idx, line in enumerate(file):
        if line == "\n":
            break
        
        if not check(line, line_idx + 1):
            print(f"Error in line {line_idx + 1} of the input code.")
            return

    print("\n Variables and it's values : ")
    # print(list_variables)
    print(variables_with_value)

if __name__ == "__main__":
    main()