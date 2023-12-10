from relational_expression import getExpression
from operators import UnaryOperator, BinaryOperator
from utility import QueryKeywords, processAttribute
import itertools

def allCombination(conditions, result_list : list[list[str]]):
    for l in range(1, len(conditions)):
        combination = list(itertools.combinations(conditions, l))
        for com in combination:
            result_list.append(com)

def cascadingOfSelection(current_node : UnaryOperator | BinaryOperator, root_node : UnaryOperator | BinaryOperator, equivalences : set[str], equivalences_list : list[str]):
    if current_node.id_name == QueryKeywords.WHERE.value and current_node.attribute:
        conditions : list[str] = []
        for condition in current_node.attribute.split('and'):
            c = processAttribute(condition)
            conditions.append(c)
        
        combinations : list[set[int]] = []
        
        allCombination(conditions, combinations)
        
        old_attribute = current_node.attribute
        child_node = current_node.child
        
        for combination in combinations:
            temp_current_node = current_node

            for index, condition in enumerate(combination):
                new_node = UnaryOperator(QueryKeywords.WHERE.value)
                new_node.attribute = condition
                
                temp_current_node.child = new_node
                new_node.root = temp_current_node
                
                temp_current_node = new_node
            
            remianing_attribute = ""
            for i in range(len(conditions)):
                if not conditions[i] in combination:
                    if remianing_attribute == "":
                        remianing_attribute = conditions[i]
                    else:
                        remianing_attribute += " and " + conditions[i]
            
            current_node.attribute = remianing_attribute
            temp_current_node.child = child_node
            child_node.root = temp_current_node
            
            recursiveEquivalences(temp_current_node.child, root_node, equivalences, equivalences_list)
            commutativityOfSelection(current_node, root_node, equivalences, equivalences_list)
            current_node.child = child_node
            child_node.root = current_node
            current_node.attribute = old_attribute

def commutativityOfSelection(current_node : UnaryOperator | BinaryOperator, root_node : UnaryOperator | BinaryOperator, equivalences : set[str], equivalences_list : list[str]):
    if isinstance(current_node, BinaryOperator) or not current_node.child:
        return

    if current_node.child and  current_node.id_name == QueryKeywords.WHERE.value and current_node.child.id_name == QueryKeywords.WHERE.value:
        parent_node = current_node.root
        child_node = current_node.child
        grand_child = child_node.child
        
        parent_node.child = child_node
        child_node.root = parent_node
        
        child_node.child = current_node
        current_node.root = child_node
        
        current_node.child = grand_child
        grand_child.root = current_node
        
        recursiveEquivalences(current_node.child, root_node, equivalences, equivalences_list)
        
        parent_node.child = current_node
        current_node.root = parent_node
        
        current_node.child = child_node
        child_node.root = current_node
        
        child_node.child = grand_child
        grand_child.root = child_node
            
def selectionDistributionOverThetaJoin(current_node : UnaryOperator | BinaryOperator, root_node : UnaryOperator | BinaryOperator, equivalences : set[str], equivalences_list : list[str]):
    if current_node.id_name == QueryKeywords.WHERE.value and current_node.child.id_name in [QueryKeywords.INNER_JOIN.value, QueryKeywords.LEFT_JOIN.value, QueryKeywords.RIGHT_JOIN.value, QueryKeywords.NATURAL_JOIN.value]:
        parent_node = current_node.root
        child_node = current_node.child
        # print(f"{parent_node} --->>> {child_node}")
        
        child_left_child = child_node.left_child
        child_right_child = child_node.right_child
        
        parent_node.child = child_node
        child_node.root = parent_node
        
        child_node.left_child = current_node
        current_node.root = child_node
        
        current_node.child = child_left_child
        child_left_child.root = current_node
        recursiveEquivalences(current_node, root_node, equivalences, equivalences_list)
        
        # reset left child
        child_node.left_child = child_left_child
        child_left_child.root = child_node
        
        # new distribute to right child
        child_node.right_child = current_node
        current_node.root = child_node
        
        current_node.child = child_right_child
        child_right_child.root = current_node
        
        recursiveEquivalences(current_node, root_node, equivalences, equivalences_list)
        
        child_node.right_child = child_right_child
        child_right_child.root = child_node
        
        parent_node.child = current_node
        current_node.root = parent_node
        
        current_node.child = child_node
        child_node.root = current_node
    
def selectionCombineWithJoin(current_node : UnaryOperator | BinaryOperator, root_node : UnaryOperator | BinaryOperator, equivalences : set[str], equivalences_list : list[str]):
     if current_node.attribute and current_node.id_name == QueryKeywords.WHERE.value and current_node.child.id_name in [QueryKeywords.INNER_JOIN.value, QueryKeywords.LEFT_JOIN.value, QueryKeywords.RIGHT_JOIN.value, QueryKeywords.NATURAL_JOIN.value]:
        child_node = current_node.child
        
        old_attrib_of_current_node = current_node.attribute
        old_attrib_of_child_node = child_node.attribute

        if child_node.attribute:
            child_node.attribute = child_node.attribute + " and " + old_attrib_of_current_node
        else:
            child_node.attribute = old_attrib_of_current_node
        
        current_node.attribute = None
        
        recursiveEquivalences(current_node.child, root_node, equivalences, equivalences_list)
        
        current_node.attribute = old_attrib_of_current_node
        child_node.attribute = old_attrib_of_child_node   

def commutativityOfJoin(current_node : UnaryOperator | BinaryOperator, root_node: UnaryOperator | BinaryOperator, equivalences : set[str], equivalences_list : list[str]):                    
    if isinstance(current_node, BinaryOperator):
        left_child = current_node.left_child
        right_child = current_node.right_child
        
        current_node.left_child = right_child
        current_node.right_child = left_child
        recursiveEquivalences(current_node.left_child, root_node, equivalences, equivalences_list)
        recursiveEquivalences(current_node.right_child, root_node, equivalences, equivalences_list)
        
        current_node.left_child = left_child
        current_node.right_child = right_child

def recursiveEquivalences(current_node : UnaryOperator | BinaryOperator, root_node : UnaryOperator | BinaryOperator, equivalences : set[str], equivalences_list : list[str]):
    if current_node == None:
        expression = getExpression(root_node)
          
        if not equivalences.__contains__(expression):
            equivalences.add(expression)
            equivalences_list.append(expression)
        return

    if isinstance(current_node, UnaryOperator):
        recursiveEquivalences(current_node.child, root_node, equivalences, equivalences_list)
    else:
        recursiveEquivalences(current_node.left_child, root_node, equivalences, equivalences_list)
        recursiveEquivalences(current_node.right_child, root_node, equivalences, equivalences_list)

    cascadingOfSelection(current_node, root_node, equivalences, equivalences_list)
    commutativityOfSelection(current_node, root_node, equivalences, equivalences_list)
    commutativityOfJoin(current_node, root_node, equivalences, equivalences_list)
    selectionDistributionOverThetaJoin(current_node, root_node, equivalences, equivalences_list)
    selectionCombineWithJoin(current_node, root_node, equivalences, equivalences_list)

def getEquivalence(root_node : UnaryOperator | BinaryOperator) -> list[str]:
    equivalences : set[str] = set()
    equivalences_list : list[str] = []

    recursiveEquivalences(root_node, root_node, equivalences, equivalences_list)

    return equivalences_list