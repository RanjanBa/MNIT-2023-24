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

def getWordsFromParenthesis(query : str) -> dict[int, int]:
    stack : list[int] = []
    
    parenthesisRelation : dict[int, int] = {}
    
    for i in range(len(query)):
        if query[i] == '(':
            stack.append(i)
        elif query[i] == ')':
            if len(stack) == 0:
                raise Exception("Given query does not have valid parenthesis!")
            j = stack.pop()
            
            if i - (j + 1) > 0:
                parenthesisRelation[j] = i
            
    if len(stack) != 0:
        raise Exception("Given query does not have valid parenthesis!")
    
    return parenthesisRelation

UNICODES = {
    "select" : u"\u03A0",
    "where" : u"\u03C3",
    "union" : u"\u03C5",
    "except" : "-",
    "intersection" : "\u2229",
    "inner join" : u"\u22C8",
    "right join" : u"\u27D6",
    "left join" : u"\u27D5",
    "natural join" : u"\u22C8",
    "cross join" : u"\u2715"
}

def getUnicode(code : str) -> str:
    if UNICODES.keys().__contains__(code):
        return UNICODES[code]
    
    return code

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

def isQueryKeywordPresent(query : str):
    for idx in range(len(query)):
        for keyword in QueryKeywords:
            if idx > 0 and query[idx-1] != " ":
                continue
            
            last = idx + len(keyword.value)
            
            if last < len(query) and query[last] != " ":
                continue
            
            new_word = query[idx:last]
            
            if new_word.lower() == keyword.value.lower():
                return True
    
    return False