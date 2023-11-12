import sys

from utility import QueryKeywords
from states import State
from operators import Operator

sys.getdefaultencoding()


def getExpression(leaf_node : Operator) -> str:
    expression = ""
    while leaf_node.id_name != QueryKeywords.SELECT.value:
        if leaf_node.id_name == QueryKeywords.WHERE.value:
            expression = "selection(" + leaf_node.attrib + ")" + expression
        elif leaf_node.id_name == QueryKeywords.ON.value:
            expression = "(" + leaf_node.attrib + ")"
        elif leaf_node.id_name in[QueryKeywords.INNER_JOIN.value, QueryKeywords.LEFT_JOIN.value, QueryKeywords.RIGHT_JOIN.value]:
            expression = f" {leaf_node.id_name} " + expression + " " + leaf_node.attrib + ")"
        elif leaf_node.id_name == QueryKeywords.NATURAL_JOIN.value:
            expression = expression + f" {leaf_node.id_name} " + leaf_node.attrib + ")"
        elif leaf_node.id_name == QueryKeywords.FROM.value:
            attrib = leaf_node.attrib.replace(" ", "")
            attrib = attrib.replace(",", " X ")
            expression = "(" + attrib + expression
            if leaf_node.child == None:
                expression += ")"
            elif not leaf_node.child.id_name in [QueryKeywords.INNER_JOIN.value, QueryKeywords.LEFT_JOIN.value, QueryKeywords.RIGHT_JOIN.value, QueryKeywords.NATURAL_JOIN.value]:
                expression += ")"
        else:
            print("not implemented")

        leaf_node = leaf_node.root
    
    if leaf_node.attrib != "*":
        expression = "projection(" + leaf_node.attrib + ")" + expression

    return expression

def convertIntoRelationalAlgebra(root_state : State, sql_query : str):
    print(f"\tSQL Query :  {sql_query}")

    cur_state = root_state
    cur_idx = 0

    expression = ""
    
    print(f"\n\tRelational Algebraic Expression :  {expression} \n")
    star = 40 * "*"
    print(f"{star: ^100}", "\n")
