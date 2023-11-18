from database_manager import saveDatabase, loadDatabase
from operators import UnaryOperator, BinaryOperator
from states import State
from utility import StateKeywords, QueryKeywords, getWordsFromParenthesis


def createFlowGraph() -> State:
    root_state = State(StateKeywords.ROOT.value)
    completed_state = State(StateKeywords.COMPLETE.value)
    error_state = State(StateKeywords.ERROR.value)
    
    create_state = State(StateKeywords.CREATE.value)
    database_state = State(StateKeywords.DATABASE.value)
    table_state = State(StateKeywords.TABLE.value)
    select_state = State(StateKeywords.SELECT.value)
    from_state = State(StateKeywords.FROM.value)
    where_state = State(StateKeywords.WHERE.value)
    inner_join_state = State(StateKeywords.INNER_JOIN.value)
    left_join_state = State(StateKeywords.LEFT_JOIN.value)
    right_join_state = State(StateKeywords.RIGHT_JOIN.value)
    natural_join_state = State(StateKeywords.NATURAL_JOIN.value)
    on_state = State(StateKeywords.ON.value)
    union_state = State(StateKeywords.UNION.value)
    intersection_state = State(StateKeywords.INTERSECTION.value)
    except_state = State(StateKeywords.EXCEPT.value)

    # define flow graph    
    root_state.next_states[QueryKeywords.CREATE.value] = create_state
    root_state.next_states[QueryKeywords.SELECT.value] = select_state
    root_state.next_states[""] = error_state
    
    create_state.next_states[QueryKeywords.DATABASE.value] = database_state
    create_state.next_states[QueryKeywords.TABLE.value] = table_state
    create_state.next_states[""] = error_state
    
    database_state.next_states[""] = completed_state
    
    table_state.next_states[""] = completed_state
    
    select_state.next_states[QueryKeywords.FROM.value] = from_state
    select_state.next_states[""] = error_state
    
    from_state.next_states[QueryKeywords.WHERE.value] = where_state
    from_state.next_states[QueryKeywords.INNER_JOIN.value] = inner_join_state
    from_state.next_states[QueryKeywords.LEFT_JOIN.value] = left_join_state
    from_state.next_states[QueryKeywords.RIGHT_JOIN.value] = right_join_state
    from_state.next_states[QueryKeywords.NATURAL_JOIN.value] = natural_join_state
    from_state.next_states[QueryKeywords.UNION.value] = union_state
    from_state.next_states[QueryKeywords.INTERSECTION.value] = intersection_state
    from_state.next_states[QueryKeywords.EXCEPT.value] = except_state
    from_state.next_states[""] = completed_state
    
    where_state.next_states[QueryKeywords.SELECT.value] = select_state
    where_state.next_states[QueryKeywords.UNION.value] = union_state
    where_state.next_states[QueryKeywords.INTERSECTION.value] = intersection_state
    where_state.next_states[QueryKeywords.EXCEPT.value] = except_state
    where_state.next_states[""] = completed_state
    
    inner_join_state.next_states[QueryKeywords.ON.value] = on_state
    inner_join_state.next_states[""] = completed_state
    
    left_join_state.next_states[QueryKeywords.ON.value] = on_state
    left_join_state.next_states[""] = completed_state
    
    right_join_state.next_states[QueryKeywords.ON.value] = on_state
    right_join_state.next_states[""] = completed_state

    natural_join_state.next_states[QueryKeywords.WHERE.value] = where_state
    natural_join_state.next_states[QueryKeywords.UNION.value] = union_state
    natural_join_state.next_states[QueryKeywords.INTERSECTION.value] = intersection_state
    natural_join_state.next_states[QueryKeywords.EXCEPT.value] = except_state
    natural_join_state.next_states[""] = completed_state

    on_state.next_states[QueryKeywords.WHERE.value] = where_state
    on_state.next_states[QueryKeywords.UNION.value] = union_state
    on_state.next_states[QueryKeywords.INTERSECTION.value] = intersection_state
    on_state.next_states[QueryKeywords.EXCEPT.value] = except_state
    on_state.next_states[""] = completed_state

    union_state.next_states[QueryKeywords.SELECT.value] = select_state
    union_state.next_states[""] = error_state
    
    intersection_state.next_states[QueryKeywords.SELECT.value] = select_state
    intersection_state.next_states[""] = error_state
    
    except_state.next_states[QueryKeywords.SELECT.value] = select_state
    except_state.next_states[""] = error_state
        
    return root_state

def processAttribute(attrib : str) -> str:
    if not attrib:
        return None
    
    attrib = attrib.strip()
    
    if len(attrib) == 0:
        return None
    
    if attrib[0] == '(':
        if len(attrib) == 1:
            return None
        
        attrib = attrib[1:]
    
    if attrib[-1] == ')':
        if len(attrib) == 1:
            return None
        
        attrib = attrib[:-1]
        
    return attrib

def getExpression(root_state : State, root_node : UnaryOperator | BinaryOperator):
    expression = ""
    
    while root_node:
        attribute = root_node.attribute
        print(attribute)
        if root_node.attribute:
            attribute = getRelationalAlgebra(root_state, root_node.attribute)
            
        if root_node.id_name == StateKeywords.SELECT.value:
            expression = root_node.id_name + f"({attribute})"
        elif root_node.id_name == StateKeywords.WHERE.value:
            expression += root_node.id_name + f"({attribute})"
        elif root_node.id_name == StateKeywords.FROM.value:
            expression += f"({attribute})"
        elif root_node.id_name in [StateKeywords.INNER_JOIN.value, StateKeywords.LEFT_JOIN.value, StateKeywords.RIGHT_JOIN.value, StateKeywords.NATURAL_JOIN.value]:
            expression += "(" + getExpression(root_state, root_node.left_child) + f" {root_node.id_name} " + f"({attribute})" + getExpression(root_state, root_node.right_child) + ")"
            break
        elif root_node.id_name in [StateKeywords.UNION.value, StateKeywords.INTERSECTION.value, StateKeywords.EXCEPT.value]:
            expression += "(" + getExpression(root_state, root_node.left_child) + ")" + f" {root_node.id_name} " + "(" + getExpression(root_state, root_node.right_child) + ")"
            break
        
        root_node = root_node.child

    return expression

def createSQLTree(root_state : State, query: str) -> UnaryOperator | BinaryOperator:
    #print("Query : ", query)
     
    _, parenthesisRelation = getWordsFromParenthesis(query)

    current_state = root_state
    start_idx = 0
    
    root_node : UnaryOperator | BinaryOperator = None
    current_select_node : UnaryOperator = None
    
    while start_idx < len(query) and current_state and not current_state.identifer in [StateKeywords.ERROR.value, StateKeywords.COMPLETE.value]:
        while(start_idx < len(query) and query[start_idx] == " "):
            start_idx += 1

        next_state, attrib = current_state.getNextStateAndCurrentStateAttribute(query, start_idx, parenthesisRelation)
        #print(f"current-state : {current_state} attribute : {attrib} \t next-state {next_state}")
        
        if next_state:
            start_idx += len(next_state.identifer)
        
        if attrib:
            start_idx += len(attrib)
            
        if attrib:
            attrib = processAttribute(attrib)
        
        if current_state.identifer != StateKeywords.ROOT.value:
            if root_node == None:
                if current_state.identifer == StateKeywords.CREATE.value:
                    root_node = UnaryOperator(StateKeywords.CREATE.value)
                elif current_state.identifer == StateKeywords.SELECT.value:
                    root_node = UnaryOperator(StateKeywords.SELECT.value)
                    root_node.attribute = attrib
                    current_select_node = root_node
                else:
                    raise Exception("Given query is not valid!")
            else:
                if current_state.identifer in [StateKeywords.DATABASE.value, StateKeywords.TABLE.value]:
                    node = UnaryOperator(current_state.identifer)
                    node.root = root_node
                    node.attribute = attrib
                    if isinstance(root_node, UnaryOperator):
                        root_node.child = node
                    else:
                        raise Exception(f"Previous node is not instance of {UnaryOperator.__name__}")
                elif current_state.identifer == StateKeywords.SELECT.value:
                    node = UnaryOperator(current_state.identifer)
                    node.attribute = attrib
                    node.root = root_node
                    root_node.right_child = node
                    current_select_node = node
                elif current_state.identifer == StateKeywords.FROM.value:
                    node = UnaryOperator(current_state.identifer)
                    node.root = current_select_node
                    node.attribute = attrib
                    if isinstance(current_select_node, UnaryOperator):
                        current_select_node.child = node
                    else:
                        raise Exception(f"Previous node is not instance of {UnaryOperator.__name__}")
                elif current_state.identifer == StateKeywords.WHERE.value:
                    node = UnaryOperator(current_state.identifer)
                    node.attribute = attrib
                    
                    child = current_select_node.child
                    
                    current_select_node.child = node
                    node.root = current_select_node
                    node.child = child
                    child.root = node
                elif current_state.identifer in [StateKeywords.INNER_JOIN.value, StateKeywords.LEFT_JOIN.value, StateKeywords.RIGHT_JOIN.value, StateKeywords.NATURAL_JOIN.value]:
                    node = BinaryOperator(current_state.identifer)
                    
                    current_node = current_select_node
                    while current_node.child.id_name != StateKeywords.FROM.value:
                        current_node = current_node.child
                    
                    from_node = current_node.child
                    from_node.root = node

                    current_node.child = node
                    node.root = current_node
                    
                    node.left_child = from_node
                    
                    from_node = UnaryOperator(StateKeywords.FROM.value)
                    from_node.attribute = attrib
                    from_node.root = node
                    
                    node.right_child = from_node
                elif current_state.identifer == StateKeywords.ON.value:
                    current_node = current_select_node
                    
                    def isPresent(id_name : str):
                        if id_name in [StateKeywords.INNER_JOIN.value, StateKeywords.LEFT_JOIN.value, StateKeywords.RIGHT_JOIN.value, StateKeywords.NATURAL_JOIN.value]:
                            return True
                        
                        return False
                    
                    while(not isPresent(current_node.id_name)):
                        current_node = current_node.child
                        
                    current_node.attribute = attrib
                elif current_state.identifer in [StateKeywords.UNION.value, StateKeywords.INTERSECTION.value, StateKeywords.EXCEPT.value]:
                    node = BinaryOperator(current_state.identifer)
                    
                    node.left_child = root_node
                    root_node.root = node
                    
                    root_node = node
        
        current_state = next_state
    
    
    if current_state.identifer == StateKeywords.ERROR.value:
        raise Exception("Given query is not valid.")
    
    return root_node

def getRelationalAlgebra(root_state : State, query : str):
    try:
        root_node = createSQLTree(root_state, query)
        return getExpression(root_state, root_node)
    except:
        return query


def parseSQLQuery(root_state : State, query : str):
    print (f"Query : {query}")
    next_state, _ = root_state.getNextStateAndCurrentStateAttribute(query, 0)
    
    if next_state.identifer == StateKeywords.CREATE.value:
        root_node = createSQLTree(root_state, query)
        child = root_node.child
        if child:
            if child.id_name == StateKeywords.TABLE.value:
                print(f"Create Table : {child.attribute}")
            elif child.id_name == StateKeywords.DATABASE.value:
                print(f"Create Database : {child.attribute}")
    else:
        print(getRelationalAlgebra(root_state, query))

def main():
    # sql_queries = [ "SELECT * FROM table",
    #    "SELECT * FROM table WHERE a = b and c = d",
    #    "SELECT c_id, c_name, c_title, d_PADD FROM table",
    #    "SELECT c_id, c_name, c_title, d_PADD FROM table WHERE b > 5000",
    #    "SELECT c_id, c_name, c_title, d_PADD FROM table_a INNER JOIN Customers ON table.id = customers.id WHERE f = g UNION SELECT c_id, c_name, c_title, d_PADD FROM table_b WHERE b > 5000 UNION SELECT c_id, c_test FROM table_c",
    #    "SELECT department_id, department_name FROM departments d WHERE department_id = d.department_id INTERSECTION SELECT * FROM table1, table2, table3",
    #    "SELECT c_id, c_name, c_title, d_PADD FROM table_a LEFT JOIN Customers ON database.id = customers.id WHERE f = g UNION SELECT c_id, c_name, c_title, d_PADD FROM table_b WHERE b > 5000 UNION SELECT c-id, c_test FROM table_c",
    #    "SELECT c_id, c_name, c_title, d_PADD FROM table_a RIGHT JOIN Customers ON database.id = customers.id WHERE f = g UNION SELECT c_id, c_name, c_title, d_PADD FROM table_b WHERE b > 5000 UNION SELECT c-id, c_test FROM table_c",
    #    "SELECT c_id, c_name FROM table_a NATURAL JOIN table_b"
    # ]

    # sql_queries = [
    #     "SELECT c_id, c_name FROM table_a INNER JOIN table_b ON table_a.c_id = table_b.c_id",
    #     "SELECT c_id, c_name FROM table_a NATURAL JOIN table_b",
    #     "SELECT * FROM table_a NATURAL JOIN table_b"
    # ]
    
    sql_queries = [
        "CREATE DATABASE database_name",
        "CREATE TABLE (attrib_1, attrib_2)",
        "SELECT c_id, c_name FROM (SELECT p_id FROM table1 WHERE (p_id < test))",
        "SELECT c_id, c_name FROM (SELECT p_id FROM table1) WHERE p_id < test",
        "SELECT c_id, c_name FROM SELECT p_id FROM table1 WHERE p_id < test"
    ]

    root_state = createFlowGraph()

    for query in sql_queries:
        parseSQLQuery(root_state, query)
        print()

if __name__ == "__main__":
    main()