from abc import ABC, abstractmethod

class Operator(ABC):
    @abstractmethod
    def __init__(self, id_name : str) -> None:
        self._id_name = id_name
        self._attrib : str = None
        self.root : Operator = None

    @property
    def id_name(self)->str:
        return self._id_name
    
    @property
    def get_attrib(self) -> str:
        return self._attrib
    
    def __str__(self) -> str:
        return f"node : {self._id_name}"


class UnaryOperator(Operator):
    def __init__(self, id_name: str) -> None:
        super.__init__(id_name)
        self._child : Operator = None
        
    def getChild(self) -> Operator:
        return self._child

class BinaryOperator(Operator):
    def __init__(self, id_name: str) -> None:
        super.__init__(id_name)
        self._left_child : Operator = None
        self._right_child : Operator = None
        
    def getLeftChild(self) -> Operator:
        return self._left_child
    
    def getRightChild(self) -> Operator:
        return self._right_child