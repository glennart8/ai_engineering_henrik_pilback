from pydantic import BaseModel, Field
import pandas as pd
from pprint import pprint


class Utbildning(BaseModel):
    utbildningsomrade: str = Field(alias='Utbildningsområde')
    sun5_inriktning: str = Field(alias='SUN5 inriktning')
    sun5_inriktning_namn: str = Field(alias='SUN5 inriktning namn')
    utbildningsnamn: str = Field(alias='Utbildningsnamn')
    beslut: str = Field(alias='Beslut')
    diarienummer: str = Field(alias='Diarienummer')
    flera_kommuner: str = Field(alias='Flera kommuner')
    antal_kommuner: int = Field(alias='Antal kommuner')
    lan: str = Field(alias='Län')
    kommun: str = Field(alias='Kommun')
    yh_poang: int = Field(alias='YH-poäng')
    studieform: str = Field(alias='Studieform')
    studietakt_procent: int = Field(alias='Studietakt %')
    typ_av_examen: str = Field(alias='Typ av examen')
    seqf_niva: int = Field(alias='SeQF nivå')
    smalt_yrkesomrade: str = Field(alias='Smalt yrkesområde')
    utbildningsanordnare: str = Field(alias='Utbildningsanordnare administrativ enhet')
    huvudmannatyp: str = Field(alias='Huvudmannatyp')
    sokta_utbildningsomgangar: int = Field(alias='Sökta utbildningsomgångar')
    beviljade_utbildningsomgangar: int = Field(alias='Beviljade utbildningsomgångar')
    sokta_platser_per_omgang: int = Field(alias='Sökta platser per utbildningsomgång')
    sokta_platser_totalt: int = Field(alias='Sökta platser totalt')
    beviljade_platser_omgang_1: int = Field(alias='Beviljade platser utbildningsomgång 1')
    beviljade_platser_omgang_2: int = Field(alias='Beviljade platser utbildningsomgång 2')
    beviljade_platser_omgang_3: int = Field(alias='Beviljade platser utbildningsomgång 3')
    beviljade_platser_omgang_4: int = Field(alias='Beviljade platser utbildningsomgång 4')
    beviljade_platser_omgang_5: int = Field(alias='Beviljade platser utbildningsomgång 5')
    beviljade_platser_totalt: int = Field(alias='Beviljade platser totalt')
    
def read_data():
    df = pd.read_excel("resultat-ansokningsomgang-2024.xlsx", sheet_name="Tabell 3", header=5)
    
    #Droppa NaN-värden som ställde till det vid valideringen
    df.dropna(inplace=True)
    
    # Gör dataframen till en DICT för att kunna validera med model_validate()
    df_dict = df.to_dict(orient='records')

    # Validera data
    validated_data = [Utbildning.model_validate(item) for item in df_dict]
    return validated_data
    
data = read_data()



