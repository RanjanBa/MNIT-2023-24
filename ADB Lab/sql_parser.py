import sys

from utility import Keywords
from states import State
from nodes import Node

sys.getdefaultencoding()

def createStateMachine() -> State:
    select_state = State(Keywords.SELECT.value)
    from_state = State(Keywords.FROM.value)
    where_state = State(Keywords.WHERE.value)
    inner_join_state = State(Keywords.INNER_JOIN.value)
    left_join_state = State(Keywords.LEFT_JOIN.value)
    right_join_state = State(Keywords.RIGHT_JOIN.value)
    natural_join_state = State(Keywords.NATURAL_JOIN.value)
    on_state = State(Keywords.ON.value)
    union_state = State(Keywords.UNION.value)
    intersection_state = State(Keywords.INTERSECTION.value)
    except_state = State(Keywords.EXCEPT.value)

    completed_state = State("completed")
    error_state = State("error")
    
    root_state = State("root")
    
    root_state.next_states[Keywords.SELECT.value] = select_state
    
    select_state.next_states[Keywords.FROM.value] = from_state
    select_state.next_states[""] = error_state
    
    from_state.next_states[Keywords.WHERE.value] = where_state
    from_state.next_states[Keywords.INNER_JOIN.value] = inner_join_state
    from_state.next_states[Keywords.LEFT_JOIN.value] = left_join_state
    from_state.next_states[Keywords.RIGHT_JOIN.value] = right_join_state
    from_state.next_states[Keywords.NATURAL_JOIN.value] = natural_join_state
    from_state.next_states[Keywords.UNION.value] = union_state
    from_state.next_states[Keywords.INTERSECTION.value] = intersection_state
    from_state.next_states[Keywords.EXCEPT.value] = except_state
    from_state.next_states[""] = completed_state
    
    where_state.next_states[Keywords.SELECT.value] = select_state
    where_state.next_states[Keywords.UNION.value] = union_state
    where_state.next_states[Keywords.INTERSECTION.value] = intersection_state
    where_state.next_states[Keywords.EXCEPT.value] = except_state
    where_state.next_states[""] = completed_state
    
    inner_join_state.next_states[Keywords.ON.value] = on_state
    
    left_join_state.next_states[Keywords.ON.value] = on_state
    
    right_join_state.next_states[Keywords.ON.value] = on_state

    natural_join_state.next_states[Keywords.WHERE.value] = where_state
    natural_join_state.next_states[Keywords.UNION.value] = union_state
    natural_join_state.next_states[Keywords.INTERSECTION.value] = intersection_state
    natural_join_state.next_states[Keywords.EXCEPT.value] = except_state
    natural_join_state.next_states[""] = completed_state

    on_state.next_states[Keywords.WHERE.value] = where_state
    on_state.next_states[Keywords.UNION.value] = union_state
    on_state.next_states[Keywords.INTERSECTION.value] = intersection_state
    on_state.next_states[Keywords.EXCEPT.value] = except_state
    on_state.next_states[""] = completed_state

    union_state.next_states[Keywords.SELECT.value] = select_state
    intersection_state.next_states[Keywords.SELECT.value] = select_state
    except_state.next_states[Keywords.SELECT.value] = select_state
    
    return root_state

def getExpression(leaf_node : Node) -> str:
    expression = ""
    while leaf_node.id_name != Keywords.SELECT.value:
        if leaf_node.id_name == Keywords.WHERE.value:
            expression = "selection(" + leaf_node.attrib + ")" + expression
        elif leaf_node.id_name == Keywords.ON.value:
            expression = "(" + leaf_node.attrib + ")"
        elif leaf_node.id_name in[Keywords.INNER_JOIN.value, Keywords.LEFT_JOIN.value, Keywords.RIGHT_JOIN.value]:
            expression = f" {leaf_node.id_name} " + expression + " " + leaf_node.attrib + ")"
        elif leaf_node.id_name == Keywords.NATURAL_JOIN.value:
            expression = expression + f" {leaf_node.id_name} " + leaf_node.attrib + ")"
        elif leaf_node.id_name == Keywords.FROM.value:
            attrib = leaf_node.attrib.replace(" ", "")
            attrib = attrib.replace(",", " X ")
            expression = "(" + attrib + expression
            if leaf_node.child == None:
                expression += ")"
            elif not leaf_node.child.id_name in [Keywords.INNER_JOIN.value, Keywords.LEFT_JOIN.value, Keywords.RIGHT_JOIN.value, Keywords.NATURAL_JOIN.value]:
                expression += ")"
        else:
            print("not implemented")

        leaf_node = leaf_node.root
    
    if leaf_node.attrib != "*":
        expression = "projection(" + leaf_node.attrib + ")" + expression

    return expression

def convertIntoRelationalAlgebra(sql_query : str):
    print(f"\tSQL Query :  {sql_query}")

    cur_idx = 0
    
    cur_state = createStateMachine()

    cur_node = None

    expression = ""
    
    while cur_state != None and cur_state.identifer != "error" and cur_state.identifer != "completed":
        state, attrib = cur_state.getNextState(sql_query[cur_idx:])

        if state == None:
            print(cur_state.identifer)
            print("error")

        cur_idx += len(attrib)

        attrib = attrib.replace("(", "").replace(")", "")
        attrib = attrib.strip()
            
        if cur_state.identifer == "root":
            cur_node = Node("root")
        elif cur_state.identifer in [Keywords.UNION.value, Keywords.INTERSECTION.value, Keywords.EXCEPT.value]:
            expression += getExpression(cur_node) + f" {cur_state.identifer} "
            cur_node = Node("root")
        else:
            new_node = Node(cur_state.identifer)
            new_node.attrib =  attrib

            if cur_state.identifer == Keywords.WHERE.value:
                temp_node = cur_node

                while temp_node.id_name != Keywords.SELECT.value:
                    temp_node = temp_node.root

                temp_child = temp_node.child
                temp_node.child = new_node
                new_node.root = temp_node

                new_node.child = temp_child
                temp_child.root = new_node
            else:
                new_node.root = cur_node
                cur_node.child = new_node

                cur_node = new_node

        cur_state = state
        cur_idx += len(cur_state.identifer)

        if state.identifer == "completed":
            expression += getExpression(cur_node)

    if cur_state.identifer == "error":
        print("\tError in query statement")
        return
    
    print(f"\n\tRelational Algebraic Expression :  {expression} \n")
    print(6*"\t",40*"*", "\n")

def main():
    #sql_queries = [ "SELECT * FROM table",
    #    "SELECT * FROM table WHERE a = b and c = d",
    #    "SELECT c_id, c_name, c_title, d_PADD FROM table",
    #    "SELECT c_id, c_name, c_title, d_PADD FROM table WHERE b > 5000",
    #    "SELECT c_id, c_name, c_title, d_PADD FROM table_a INNER JOIN Customers ON table.id = customers.id WHERE f = g UNION SELECT c_id, c_name, c_title, d_PADD FROM table_b WHERE b > 5000 UNION SELECT c_id, c_test FROM table_c",
    #   "SELECT department_id, department_name FROM departments d WHERE department_id = d.department_id INTERSECTION SELECT * FROM table1, table2, table3",
    #    "SELECT c_id, c_name, c_title, d_PADD FROM table_a LEFT JOIN Customers ON database.id = customers.id WHERE f = g UNION SELECT c_id, c_name, c_title, d_PADD FROM table_b WHERE b > 5000 UNION SELECT c-id, c_test FROM table_c",
    #    "SELECT c_id, c_name, c_title, d_PADD FROM table_a RIGHT JOIN Customers ON database.id = customers.id WHERE f = g UNION SELECT c_id, c_name, c_title, d_PADD FROM table_b WHERE b > 5000 UNION SELECT c-id, c_test FROM table_c",
    #    "SELECT c_id, c_name FROM table_a NATURAL JOIN table_b"
    #]

    sql_queries = [
        "SELECT c_id, c_name FROM table_a INNER JOIN table_b ON table_a.c_id = table_b.c_id",
        "SELECT c_id, c_name FROM table_a NATURAL JOIN table_b",
        "SELECT * FROM table_a NATURAL JOIN table_b"
    ]

    for query in sql_queries:
        convertIntoRelationalAlgebra(query)

if __name__ == "__main__":
    main()
