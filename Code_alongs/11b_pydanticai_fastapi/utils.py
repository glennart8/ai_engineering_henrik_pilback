from pathlib import Path
import duckdb

DATA_PATH = Path(__file__).parent / "data"

DATA_PATH.mkdir(exist_ok=True)

# def query_duckdb(sql_code, parameters = None):
#     with duckdb.connect(DATA_PATH / "movies.duckdb") as con:
#         cursor = con.execute(sql_code, parameters)
        
#         sql_code = sql_code.strip().casefold()
        
#         if sql_code.startswith(("select", "desc;", "from", "pragma")):
#             return cursor.df()
    
    
def query_duckdb(sql_code, parameters=None):
    with duckdb.connect(str(DATA_PATH / "movies.duckdb")) as con:
        return con.execute(sql_code, parameters).df() # kör frågan och returnerar resultatet som en Df direkt