from typing import Any, List, NoReturn
import aiosqlite

# DBSearch Class -> Built for future-proofing in case I switch to SQLite-based design in the future
class DBSearch:
    fileName: str

    def __init__(self, fileName: str) -> None:
        self.fileName = fileName
    
    def generate_command(self, table_name: str, **kwargs) -> str:
        """Generate SQL command to create a table with given table name and attributes"""

        command = f"CREATE TABLE {table_name}"
        counter = 0

        for key, value in kwargs.items():
            if counter == 0:
                command = f"{command} ({key} {value}"
            else:
                command = f"{command}, {key} {value}"
            
            counter += 1
        
        if counter > 0:
            command = f"{command})"
        
        return command
    
    async def query_data(self, query: str) -> Any:
        """ASYNC --- Method to query database at self.fileName with input SQL query"""

        async with aiosqlite.connect(self.fileName) as connection:
            async with connection.cursor() as cursor:
                return await cursor.execute(query).fetchall() 
    
    async def get_data_filtered(self, table_name: str, operator: str, *args, **kwargs) -> List[Any]:
        """ASYNC --- Method to perform a filtered query with attributes specified in the given table"""

        argsString = ",".join(args)
        conditions = [f"{key} {value}" for key, value in kwargs.items()]
        filterString = f"{operator} ".join(conditions)

        async with aiosqlite.connect(self.fileName) as connection:
            async with connection.cursor() as cursor:
                return await cursor.execute(f"SELECT {argsString} FROM {table_name} WHERE {filterString}").fetchall() 
    
    async def get_data(self, table_name: str, *args) -> List[Any]:
        """ASYNC --- Method to perform unfiltered query in given table"""

        argsString = ",".join(args)

        async with aiosqlite.connect(self.fileName) as connection:
            async with connection.cursor() as cursor:
                return await cursor.execute(f"SELECT {argsString} FROM {table_name}").fetchall() 
    
    async def create_table(self, table_name: str, **kwargs) -> NoReturn:
        """ASYNC --- Method to create a table with specified table name and specified attributes"""
        
        async with aiosqlite.connect(self.fileName) as connection:
            async with connection.cursor() as cursor:
                command = self.generate_command(table_name, kwargs)
                await cursor.execute(command)
    
    async def insert_data(self, table_name, fields: List[str], data) -> NoReturn:
        """ASYNC --- Method to insert data into specified table with the given values"""

        values = ["?" for _ in fields]
        fields = ",".join(fields)
        values = ",".join(values)

        async with aiosqlite.connect(self.fileName) as connection:
            connection.executemany(f"INSERT INTO {table_name} ({fields}) values ({values})", data)