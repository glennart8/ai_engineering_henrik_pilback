from constants import DATA_PATH
import pandas as pd 
import json

df = pd.read_csv(DATA_PATH / "Sales.csv")

# Skapar en klass med en limit på 100 inhämtade varje gång en instans av klassen kallas
class DataExplorer:
    def __init__(self, limit = 100):
        self._df = df.head(limit) # _df = PRIVAT ATTRIBUT
        self._df_full = df
        
    # Returnerar variabeln (backing variable) 
    @property
    def df(self):
        return self._df
    
    # En funktion som kör describe och, samt droppar några kolumner
    def summary(self):
        self._df = (
            self._df_full.describe()
            .T.drop(["count"], axis=1)
            .drop(["Day", "Year"])
            .reset_index()
        )
        return self
    
    def kpis(self, country: str):
        """Filter out kpis based on country"""
        df_by_country = self._df_full.query("Country.str.casefold() == @country.casefold()")
        
        return {
            "total_profit": str(df_by_country["Profit"].sum()), # Var tvungen att skicka en sträng
            "total_cost": str(df_by_country["Cost"].sum()),
            "number_of_purchases": str(len(df_by_country))
        }
        
    
    # Gör om data frame till JSON för att API:et ska kunna ta emot det
    def json_response(self):
        json_data = self.df.to_json(orient = "records") # "records" ger resultat i rader och inte i kolumner
        return json.loads(json_data) # Deserialize så att det blir en lista av dictionaries i stället för json-string

if __name__ == "__main__":
    data_explorer = DataExplorer() # Skapar en instans av klassen

# print(data_explorer.df)
# pprint(data_explorer.json_response())