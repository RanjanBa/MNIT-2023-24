from utility import Keywords, findWordIndex

class State:
    def __init__(self, identifier : str) -> None:
        self.__identifier = identifier
        self.next_states : dict[str, State] = {}
        
    @property
    def identifer(self):
        return self.__identifier
    
    def getNextState(self, string : str):
        least_index = 1000000000
        
        key = ""
        
        for w in [k.value for k in Keywords]:
            idx = findWordIndex(string, w, 0)
            
            if idx == -1:
                continue
            
            if idx < least_index:
                least_index = idx
                key = w
        
        attrib = ""
        if key in self.next_states.keys():
            if least_index > 0:
                attrib = string[0:min(least_index, len(string))]

            return self.next_states[key], attrib
        
        return None, attrib
    
    def __str__(self) -> str:
        return f"state: {self.identifer}"