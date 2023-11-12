from database_manager import saveDatabase, loadDatabase
from database import Database, Table
from states import State
from utility import StateKeywords, QueryKeywords


def createFlowGraph() -> State:
    root_state = State(StateKeywords.ROOT.value)
    completed_state = State(StateKeywords.COMPLETE.value)
    error_state = State(StateKeywords.ERROR.value)
    
    create_state = State(StateKeywords.CREATE.value)
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
    
    left_join_state.next_states[QueryKeywords.ON.value] = on_state
    
    right_join_state.next_states[QueryKeywords.ON.value] = on_state

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
    intersection_state.next_states[QueryKeywords.SELECT.value] = select_state
    except_state.next_states[QueryKeywords.SELECT.value] = select_state
    
    return root_state

def parseSQLQuery(root_state, query: str):
    database_name = "test_database"
    database = Database(database_name)
    
    student_table = Table('student')
    faculty_table = Table("faculty")
    
    database.addTable(student_table)
    database.addTable(faculty_table)
    
    saveDatabase(database)
    
    loaded_database = loadDatabase(database_name)
    
    if loaded_database:
        print(loaded_database.database_name)
        for table in loaded_database.tables:
            print(table.table_name)

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

    root_state = createFlowGraph()

    for query in sql_queries:
        parseSQLQuery(root_state, query)

if __name__ == "__main__":
    main()