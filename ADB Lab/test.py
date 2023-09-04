import sys
sys.getdefaultencoding()

statement = "SELECT c-id, c_name, c_title, d_PADD FROM databse WHERE b > 5000"
#statement = "SELECT c-id, c_name, c_title, d_PADD FROM databse INNER JOIN Customers on database.id = customers.id"

# statement = input()

words = statement.split()

if words[0].upper() == "SELECT":
    idx = 1
    attribs = []
    while words[idx] != "FROM" and idx < len(words):
        w = words[idx]
        if w[-1] == ',':
            w = words[idx][0:-1]

        attribs.append(w)
        idx += 1

    idx += 1

    table_name = words[idx]

    algebric_expression = "\u03C0("

    for i in range(len(attribs)):
        algebric_expression += attribs[i]

        if(i < len(attribs) - 1):
            algebric_expression += ", "

    algebric_expression += ")"

    idx += 1

    condition = ""
    if words[idx].upper() == "WHERE":
        idx += 1
        while idx < len(words):
            condition += words[idx]
            if idx < len(words) - 1:
                condition += " "
            
            idx += 1

        algebric_expression += "\u03C3("
        
        algebric_expression += condition + ")"

        algebric_expression += "(" + table_name + ")"
    elif words[idx].upper() == "INNER" and words[idx + 1].upper() == "JOIN":
        idx += 2

        second_table_name = words[idx]

        idx += 2

        while idx < len(words):
            condition += words[idx]
            if idx < len(words) - 1:
                condition += " "
            
            idx += 1

        algebric_expression += "\u03C3("
        
        algebric_expression += condition + ")"

        algebric_expression += "(" + table_name + "\u2A1D" + second_table_name + ")"

    print(algebric_expression)
elif words[0] == "SET":
    pass