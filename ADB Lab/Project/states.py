class State:
    def __init__(self, identifier : str) -> None:
        self.__identifier = identifier
        self.next_states : dict[str, State] = {}
        
    @property
    def identifer(self):
        return self.__identifier
    
    def getNextStateAndCurrentStateAttribute(self, query : str, start_idx : int, parenthesisRelation : dict[int, int] = {}):
        key = ""
        
        if start_idx > len(query):
            return self.next_states[key], None
        
        next_states_identifiers = list(self.next_states.keys())
        
        if "" in next_states_identifiers:
            next_states_identifiers.remove("")
            
        #print(next_states_identifiers)
        
        idx : int = start_idx
        
        isFound : bool = False
        while idx < len(query) and not isFound:
            if query[idx] == "(":
                if idx in parenthesisRelation.keys():
                    idx = parenthesisRelation[idx]
                else:
                    raise Exception("Given query is not valid!")
            elif query[idx] != " " and query[idx] != ")":
                for word in next_states_identifiers:
                    if idx + len(word) > len(query):
                        continue

                    new_word = query[idx : idx + len(word)]
                    #print(new_word, word)
                    
                    if new_word.lower() == word.lower():
                        if idx + len(word) >= len(query) or query[idx + len(word)] in [" ", ")"]:
                            key = word
                            isFound = True
                            break
                        
            idx += 1
        
        if isFound:
            idx -= 1

        attrib = None
        if idx > start_idx:
            attrib = query[start_idx : idx]
        
        return self.next_states[key], attrib
            
    def __str__(self) -> str:
        return f"{self.identifer}"