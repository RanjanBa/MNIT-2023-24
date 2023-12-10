from abc import ABC, abstractmethod

class Operator(ABC):
    @abstractmethod
    def __init__(self, id_name : str) -> None:
        self._id_name = id_name
        self._attrib : str = None
        self.root : Operator = None
        self.__sub_tree : Operator = None

    @property
    def id_name(self)->str:
        return self._id_name
    
    @property
    def attribute(self) -> str:
        return self._attrib
    
    @attribute.setter
    def attribute(self, attrib : str):
        self._attrib = attrib
    
    def __str__(self) -> str:
        return f"{self._id_name}"

    @property
    def sub_tree(self):
        return self.__sub_tree
    
    @sub_tree.setter
    def sub_tree(self, tree):
        self.__sub_tree = tree
        

class UnaryOperator(Operator):
    def __init__(self, id_name: str) -> None:
        super().__init__(id_name)
        self._child : Operator = None
        
    @property
    def child(self) -> Operator:
        return self._child
    
    @child.setter
    def child(self, child : Operator):
        self._child = child
    

class BinaryOperator(Operator):
    def __init__(self, id_name: str) -> None:
        super().__init__(id_name)
        self._left_child : Operator = None
        self._right_child : Operator = None
    
    @property
    def left_child(self) -> Operator:
        return self._left_child
    
    @left_child.setter
    def left_child(self, child : Operator):
        self._left_child = child
    
    @property
    def right_child(self) -> Operator:
        return self._right_child
    
    @right_child.setter
    def right_child(self, child : Operator):
        self._right_child = child
    