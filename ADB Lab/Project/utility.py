from enum import Enum

class QueryKeywords(Enum):
    CREATE = "create"
    DATABASE = "database"
    TABLE = "table"
    SELECT = "select"
    FROM = "from"
    WHERE = "where"
    INNER_JOIN = "inner join"
    LEFT_JOIN = "left join"
    RIGHT_JOIN = "right join"
    NATURAL_JOIN = "natural join"
    ON = "on"
    UNION = "union"
    INTERSECTION = "intersection"
    EXCEPT = "except"
    
class StateKeywords(Enum):
    ROOT = "root"
    COMPLETE = "complete"
    ERROR = "error"
    CREATE = "create"
    DATABASE = "database"
    TABLE = "table"
    SELECT = "select"
    FROM = "from"
    WHERE = "where"
    INNER_JOIN = "inner join"
    LEFT_JOIN = "left join"
    RIGHT_JOIN = "right join"
    NATURAL_JOIN = "natural join"
    ON = "on"
    UNION = "union"
    INTERSECTION = "intersection"
    EXCEPT = "except"

def isValidParenthesis(query : str) -> bool:
    stack : list[int] = []
    
    for i in range(len(query)):
        if query[i] == '(':
            stack.append(i)
        elif query[i] == ')':
            if len(stack) == 0:
                return False
            stack.pop()
            
    if len(stack) == 0:
        return True
    
    return False

def getWordsFromParenthesis(query : str) -> list[str]:
    stack : list[int] = []
    
    words : list[str] = []
    parenthesisRelation : dict[int, int] = {}
    
    for i in range(len(query)):
        if query[i] == '(':
            stack.append(i)
        elif query[i] == ')':
            if len(stack) == 0:
                raise Exception("Given query does not have valid parenthesis!")
            j = stack.pop()
            
            if i - (j + 1) > 0:
                words.append(query[j+1:i])
                parenthesisRelation[j] = i
            
    if len(stack) != 0:
        raise Exception("Given query does not have valid parenthesis!")
    
    return words, parenthesisRelation
    