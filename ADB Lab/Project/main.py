from operators import UnaryOperator, BinaryOperator
from states import State
from utility import StateKeywords, QueryKeywords, getWordsFromParenthesis, isQueryKeywordPresent, processAttribute
from relational_expression import getExpression
from relational_equivalence import getEquivalence

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

def createSQLTree(root_state : State, query: str) -> UnaryOperator | BinaryOperator:
    # print("Query : ", query)
     
    parenthesisRelation = getWordsFromParenthesis(query)

    current_state = root_state
    start_idx = 0
    
    root_node : UnaryOperator | BinaryOperator = None
    current_select_node : UnaryOperator = None
    
    while start_idx < len(query) and current_state:
        while(start_idx < len(query) and query[start_idx] == " "):
            start_idx += 1

        next_state, attrib = current_state.getNextStateAndCurrentStateAttribute(query, start_idx, parenthesisRelation)
        # print(f"current-state : {current_state} attribute : {attrib} \t next-state {next_state}")
        
        if next_state:
            start_idx += len(next_state.identifer)
        
        if attrib:
            start_idx += len(attrib)
            
        if attrib:
            attrib = processAttribute(attrib)
        
        if current_state.identifer != StateKeywords.ROOT.value:
            if root_node == None:
                if current_state.identifer == StateKeywords.CREATE.value:
                    new_node = UnaryOperator(StateKeywords.CREATE.value)
                    root_node = new_node
                elif current_state.identifer == StateKeywords.SELECT.value:
                    new_node = UnaryOperator(StateKeywords.SELECT.value)
                    new_node.attribute = attrib
                    if new_node.attribute and isQueryKeywordPresent(new_node.attribute):
                        try:
                            sub_tree = createSQLTree(root_state, new_node.attribute)
                            new_node.sub_tree = sub_tree
                        except:
                            raise Exception(f"QueryKeyword : {new_node.id_name}, Nested Qury \"{attrib}\" is not valid.")

                    root_node = new_node
                    current_select_node = root_node
                else:
                    raise Exception("Given query is not valid!")
            else:
                if current_state.identifer in [StateKeywords.DATABASE.value, StateKeywords.TABLE.value]:
                    new_node = UnaryOperator(current_state.identifer)
                    new_node.attribute = attrib
                    
                    if isQueryKeywordPresent(new_node.attribute):
                        raise Exception(f"Attribute names [{attrib}] can't be Query Keywords.")
                            
                    new_node.root = root_node
                    
                    if isinstance(root_node, UnaryOperator):
                        root_node.child = new_node
                    else:
                        raise Exception(f"Previous node is not instance of {UnaryOperator.__name__}")
                elif current_state.identifer == StateKeywords.SELECT.value:
                    new_node = UnaryOperator(current_state.identifer)
                    new_node.attribute = attrib
                    
                    if new_node.attribute and isQueryKeywordPresent(new_node.attribute):
                        try:
                            sub_tree = createSQLTree(root_state, new_node.attribute)
                            new_node.sub_tree = sub_tree
                        except:
                            raise Exception(f"QueryKeyword : {new_node.id_name}, Nested Qury \"{attrib}\" is not valid.")
                    
                    new_node.root = root_node
                    root_node.right_child = new_node
                    current_select_node = new_node
                elif current_state.identifer == StateKeywords.FROM.value:
                    new_node = UnaryOperator(current_state.identifer)
                    new_node.attribute = attrib
                    
                    if new_node.attribute and isQueryKeywordPresent(new_node.attribute):
                        try:
                            sub_tree = createSQLTree(root_state, new_node.attribute)
                            new_node.sub_tree = sub_tree
                        except:
                            raise Exception(f"QueryKeyword : {new_node.id_name}, Nested Qury \"{attrib}\" is not valid.")
                    
                    new_node.root = current_select_node
                    if isinstance(current_select_node, UnaryOperator):
                        current_select_node.child = new_node
                    else:
                        raise Exception(f"Previous node is not instance of {UnaryOperator.__name__}")
                elif current_state.identifer == StateKeywords.WHERE.value:
                    new_node = UnaryOperator(current_state.identifer)
                    new_node.attribute = attrib
                    
                    if new_node.attribute and isQueryKeywordPresent(new_node.attribute):
                        try:
                            sub_tree = createSQLTree(root_state, new_node.attribute)
                            new_node.sub_tree = sub_tree
                        except:
                            raise Exception(f"QueryKeyword : {new_node.id_name}, Nested Qury \"{attrib}\" is not valid.")
                    
                    child = current_select_node.child
                    
                    current_select_node.child = new_node
                    new_node.root = current_select_node
                    new_node.child = child
                    child.root = new_node
                elif current_state.identifer in [StateKeywords.INNER_JOIN.value, StateKeywords.LEFT_JOIN.value, StateKeywords.RIGHT_JOIN.value, StateKeywords.NATURAL_JOIN.value]:
                    new_node = BinaryOperator(current_state.identifer)
                    
                    current_node = current_select_node
                    while current_node.child.id_name != StateKeywords.FROM.value:
                        current_node = current_node.child
                    
                    from_node = current_node.child
                    from_node.root = new_node

                    current_node.child = new_node
                    new_node.root = current_node
                    
                    new_node.left_child = from_node
                    
                    from_node = UnaryOperator(StateKeywords.FROM.value)
                    from_node.attribute = attrib
                    
                    if from_node.attribute and isQueryKeywordPresent(from_node.attribute) :
                        try:
                            sub_tree = createSQLTree(root_state, from_node.attribute)
                            from_node.sub_tree = sub_tree
                        except:
                            raise Exception(f"QueryKeyword : {new_node.id_name}, Nested Qury \"{attrib}\" is not valid.")
                    
                    from_node.root = new_node
                    new_node.right_child = from_node
                elif current_state.identifer == StateKeywords.ON.value:
                    current_node = current_select_node
                    
                    def isPresent(id_name : str):
                        if id_name in [StateKeywords.INNER_JOIN.value, StateKeywords.LEFT_JOIN.value, StateKeywords.RIGHT_JOIN.value, StateKeywords.NATURAL_JOIN.value]:
                            return True
                        
                        return False
                    
                    while(not isPresent(current_node.id_name)):
                        current_node = current_node.child
                        
                    current_node.attribute = attrib
                    
                    if current_node.attribute and isQueryKeywordPresent(current_node.attribute):
                        try:
                            sub_tree = createSQLTree(root_state, current_node.attribute)
                            current_node.sub_tree = sub_tree
                        except:
                            raise Exception(f"QueryKeyword : {new_node.id_name}, Nested Qury \"{attrib}\" is not valid.")
                    
                elif current_state.identifer in [StateKeywords.UNION.value, StateKeywords.INTERSECTION.value, StateKeywords.EXCEPT.value]:
                    new_node = BinaryOperator(current_state.identifer)
                    
                    new_node.left_child = root_node
                    root_node.root = new_node
                    
                    root_node = new_node
        
        current_state = next_state
        if current_state.identifer in [StateKeywords.ERROR.value, StateKeywords.COMPLETE.value]:
            break
    
    if current_state.identifer == StateKeywords.ERROR.value:
        raise Exception("Given query is not valid.")
    
    return root_node

def getRelationalAlgebra(root_state : State, query : str):
    if not isQueryKeywordPresent(query):
        return query
    
    try:
        root_node = createSQLTree(root_state, query)
        # print(f"Table Name for \"{query}\" : {getTableNames(root_state, root_node)}")
        return getExpression(root_node)
    except Exception as e:
        raise Exception(e)

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
        try:
            # str = getRelationalAlgebra(root_state, query)
            # print(str)
            root_node = createSQLTree(root_state, query)
            equivalences = getEquivalence(root_node)
            
            print("\nEquivalences : ")
            for e in equivalences:
                print("\t" + e)

            print("\nOld Expression : ") 
            print("\t" + getExpression(root_node))
        except Exception as e:
            print(e)

def main():
    file_name = "sql_query.txt"
    
    sql_queries = []
    
    with open(file_name, 'r') as file:
        for l in file:
            start_idx = 0
            while start_idx < len(l) and l[start_idx] in ['\n', ' ', ',', '#', '"', ';']:
                start_idx += 1
            
            last_idx = len(l) - 1
            while last_idx >= 0 and l[last_idx] in ['\n', ' ', ',', '#', '"', ';']:
                last_idx -= 1
            
            if start_idx <= last_idx:
                l = l[start_idx:last_idx+1]
                sql_queries.append(l)
            else:
                break

    root_state = createFlowGraph()


    for query in sql_queries:
        parseSQLQuery(root_state, query)
        print()

if __name__ == "__main__":
    main()