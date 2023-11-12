import pickle
from database import Database, Table

def createDatabase(database_name : str, tables : list[Table]):
    database = Database(database_name)
    
    for table in tables:
        database.addTable(table)
        
    return database
    
def createTable(table_name: str, attributes : list[str]):
    table = Table(table_name)
    
    for attrib in attributes:
        table.addAttribute(attrib)
    
    return table

def saveDatabase(database : Database):
    with open(database.database_name + '.pkl', 'wb') as file:
        pickle.dump(database, file)
        print(f'Database successfully saved to {database.database_name}.pkl file!')

def loadDatabase(database_name : str) -> Database:
    with open(database_name + '.pkl', 'rb') as file:
        database = pickle.load(file)
        print(f'Database successfully loaded!')
        
        return database
    
    return None