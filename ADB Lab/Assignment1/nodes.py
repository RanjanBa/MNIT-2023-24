class Node:
    def __init__(self, id_name : str) -> None:
        self.__id_name = id_name
        self.root : Node = None
        self.child : Node = None
        self.attrib : str = ""

    @property
    def id_name(self)->str:
        return self.__id_name
    
    def __str__(self) -> str:
        return f"node : {self.__id_name}"
