class Database:
    def __init__(self, database_name : str) -> None:
        self.__database_name : str = database_name
        self.__tables : list[Table] = []

    def addTable(self, table) -> None:
        self.__tables.append(table)
        
    @property
    def database_name(self) -> str:
        return self.__database_name
    
    @property
    def tables(self):
        return self.__tables


class Table:
    def __init__(self, table_name: str) -> None:
        self.__table_name = table_name
        self.__attributes : list[str] = []
        
    def addAttribute(self, attrib : str) -> None:
        self.__attributes.append(attrib)
        
    @property
    def attributes(self) -> list[str]:
        return self.__attributes
    
    @property
    def table_name(self) -> str:
        return self.__table_name
        