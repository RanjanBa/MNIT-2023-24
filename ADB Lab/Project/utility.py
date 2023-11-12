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

def findWordIndex(statement : str, word : str, start_idx : int = 0):
    if start_idx >= len(statement):
        return -1

    result = -1

    for idx in range(start_idx, len(statement)):
        found = True
        if idx > 0 and not statement[idx - 1] in [" ","("]:
            continue
        
        for i in range(0, len(word)):
            if idx + i >= len(statement) or statement[idx + i].lower() != word[i].lower():
                idx = idx + i + 1
                found = False
                break

        if found:
            if idx + len(word) < len(statement) and statement[idx + len(word)] in [" ", ")"]:
                return idx
            else:
                idx += len(word)

    return -1
