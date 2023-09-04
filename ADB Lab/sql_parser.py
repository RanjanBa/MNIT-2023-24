import sys

from utility import Keywords, findWordIndex
from states import State

sys.getdefaultencoding()

def createStateMachine():
    select_state = State(Keywords.SELECT.value)
    from_state = State(Keywords.FROM.value)
    where_state = State(Keywords.WHERE.value)
    inner_join_state = State(Keywords.INNER_JOIN.value)
    on_state = State(Keywords.ON.value)
    
    completed_state = State("completed")
    error_state = State("error")
    
    updation_state = State(Keywords.UPDATION.value)
    
    root_state = State("root")
    
    root_state.next_states[Keywords.SELECT.value] = select_state
    root_state.next_states[Keywords.UPDATION.value] = updation_state
    
    select_state.next_states[Keywords.FROM.value] = from_state
    select_state.next_states[""] = error_state
    
    from_state.next_states[Keywords.WHERE.value] = where_state
    from_state.next_states[Keywords.INNER_JOIN.value] = inner_join_state
    from_state.next_states[""] = completed_state
    
    where_state.next_states[""] = completed_state
    where_state.next_states[Keywords.SELECT.value] = select_state
    
    inner_join_state.next_states[Keywords.ON.value] = on_state
    
    on_state.next_states[""] = completed_state
    
    return root_state

def main():
    statement = "SELECT * FROM databse"
    #statement = "SELECT c-id, c_name, c_title, d_PADD FROM databse"
    #statement = "SELECT c-id, c_name, c_title, d_PADD FROM databse WHERE b > 5000"
    #statement = "SELECT c-id, c_name, c_title, d_PADD FROM databse INNER JOIN Customers ON database.id = customers.id"
    #statement =  "SELECT department_id, department_name FROM departments d WHERE NOT EXISTS (SELECT ’X’ FROM employees WHERE department_id = d.department_id)"
    
    cur_idx = 0
    
    cur_state = createStateMachine()
    
    while cur_state != None and cur_state.identifer != "error" and cur_state.identifer != "completed":
        state, attrib = cur_state.getNextState(statement[cur_idx:])
        
        cur_state = state
        
        cur_idx += len(cur_state.identifer)
        
        if attrib != None:
            cur_idx += len(attrib)
            
            attrib = attrib.replace("(", "").replace(")", "")
            
            attrib = attrib.strip()
        
        print(f"attrib : {attrib}")
        print(state)
    
if __name__ == "__main__":
    main()