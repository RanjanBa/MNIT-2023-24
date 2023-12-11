from operators import UnaryOperator, BinaryOperator
from utility import StateKeywords, getUnicode, getWordsFromParenthesis

def processFromAttribute(attribute : str):
    tables = attribute.split(',')
    
    new_attribute = ""
    for table in tables:
        if new_attribute == "":
            new_attribute = table
        else:
            new_attribute += f" {getUnicode('cross join')}" + table

    if len(tables) > 1:
        new_attribute = f"({new_attribute})"

    return new_attribute

def recursivelyGetExpression(root_node : UnaryOperator | BinaryOperator) -> str:
    if root_node == None:
        return ""
    
    expression = ""

    attribute = root_node.attribute
    if root_node.sub_tree:
        attribute = recursivelyGetExpression(root_node.sub_tree)

    if root_node.id_name == StateKeywords.SELECT.value:
        if attribute and attribute != "*":
            expression = getUnicode(root_node.id_name) + "(" + attribute + ")(" + recursivelyGetExpression(root_node.child) + ")"
        else:
            expression = recursivelyGetExpression(root_node.child)
    elif root_node.id_name == StateKeywords.WHERE.value:
        if attribute:
            expression = getUnicode(root_node.id_name) + "(" + attribute + ")(" + recursivelyGetExpression(root_node.child) + ")"
        else:
            expression = recursivelyGetExpression(root_node.child)
    elif root_node.id_name == StateKeywords.FROM.value:
        if root_node.sub_tree:
            expression = f"({attribute})"
        else:
            expression = processFromAttribute(attribute)
    elif root_node.id_name in [StateKeywords.INNER_JOIN.value, StateKeywords.LEFT_JOIN.value, StateKeywords.RIGHT_JOIN.value, StateKeywords.NATURAL_JOIN.value]:
        if attribute == None:
            expression = recursivelyGetExpression(root_node.left_child) + f" {getUnicode(root_node.id_name)} " + recursivelyGetExpression(root_node.right_child)
        else:
            expression = recursivelyGetExpression(root_node.left_child) + f" {getUnicode(root_node.id_name)} ({attribute})" + recursivelyGetExpression(root_node.right_child)
    elif root_node.id_name in [StateKeywords.UNION.value, StateKeywords.INTERSECTION.value, StateKeywords.EXCEPT.value]:
        expression = "(" + recursivelyGetExpression(root_node.left_child) + ")" + f" {getUnicode(root_node.id_name)} " + "(" + recursivelyGetExpression(root_node.right_child) + ")"

    return expression

def getExpression(root_node : UnaryOperator | BinaryOperator) -> str:
    expression = recursivelyGetExpression(root_node)
    
    relation = getWordsFromParenthesis(expression)
    
    ### remove redundent brackets
    idx = 0
    length = len(expression)
    while idx < length:
        if not relation.__contains__(idx):
            break
        if relation[idx] != length - 1 - idx:
            break
        
        idx += 1
    
    if idx < length - idx:
        expression = expression[idx: length-idx]
    
    should_run = True
    while should_run:
        relation = getWordsFromParenthesis(expression)
        length = len(expression)
        should_run = False
        for index in range(length):
            if relation.__contains__(index) and relation.__contains__(index+1):
                if relation[index] == relation[index + 1] + 1:
                    new_expression = ""
                    if index > 0:
                        new_expression = expression[0:index]
                    if index + 1 < length:
                        new_expression += expression[index + 1: relation[index]]
                    if relation[index] + 1 < length:
                        new_expression += expression[relation[index] + 1:]
                    expression = new_expression
                    should_run = True
    
    return expression

def getTableNames(root_node : UnaryOperator | BinaryOperator):
    if root_node == None:
        return None

    table_names = ""
    if root_node.id_name == StateKeywords.FROM.value:
        if root_node.sub_tree:
            return getTableNames(root_node.sub_tree)
        else:
            return root_node.attribute
    else:
        if root_node.sub_tree:
            table_names = getTableNames(root_node.sub_tree)
    
    if isinstance(root_node, UnaryOperator):
        if table_names == "":
            return getTableNames(root_node.child)
        else:
            return table_names + "," + getTableNames(root_node.child)
    
    if table_names == "":
        return getTableNames(root_node.left_child) + "," + getTableNames(root_node.right_child)
    else:
        return table_names + "," + getTableNames(root_node.left_child) + "," + getTableNames(root_node.right_child)
