from fastapi import FastAPI, Query, HTTPException
from data_processing import read_data


data = read_data()

app = FastAPI()

# Visa alla utbildningar
@app.get("/utbildning")
def get_all_educations():
    return data

# Filtrera efter skola
@app.get("/skola")
def get_from_school(skola: str):
    list_by_school = [item for item in data if item.utbildningsanordnare == skola]
    if list_by_school:
        return list_by_school
    else:
        raise HTTPException(404, detail="Inga utbildningar för denna skola")
    
@app.get("/utbildningsomrade")
def get_by_utbildningsomrade(target: str):
    list_by_field = [item for item in data if item.utbildningsomrade == target]
    if list_by_field:
        return list_by_field
    else:
        raise HTTPException(404, detail="Inget utbildningsområde hittades")
    
#E) Skapa endpoints för beviljade och avslagna utbildningar

@app.get("/beviljade")
def get_approved():
    list_by_approved = [item for item in data if item.beslut == "Beviljad"]
    if list_by_approved:
        return list_by_approved
    else:
        raise HTTPException(404, detail="Inga beviljade utbildningar")
    
@app.get("/avslagna")
def get_disapproved():
    list_by_disapproved = [item for item in data if item.beslut == "Avslag"]
    if list_by_disapproved:
        return list_by_disapproved
    else:
        raise HTTPException(404, detail="Inga avslagna utbildningar")

# KPI - NUMBERS!!
# Beräknar och returnerar det totala antalet beviljade platser i hela datasetet

@app.get("/kpi/beviljade-platser-totalt")
def get_total_approved():
    total_approved = [item for item in data if item.beslut == "Beviljad"]
    if total_approved:
        numbers_approved = sum([item.beviljade_platser_totalt for item in total_approved])
        return numbers_approved
    else:
        raise HTTPException(404, detail="Inga beviljade platser hittades")
    
# F) Another KPI
# Beräkna antalet sökta platser som fått avslag, summera och visa
@app.get("/kpi/avslagna-platser-totalt")
def get_total_disapproved():
    total_disapproved = [item for item in data if item.beslut == "Avslag"]
    if total_disapproved:
        numbers_disapproved = sum([item.sokta_platser_totalt for item in total_disapproved])
        return numbers_disapproved
    else:
        raise HTTPException(404, detail="Inga avslagna platser hittades")
        
# Visa antalet beviljade sökningar efter fält, t.ex. Data/IT

@app.get("/beviljade-efter-fält")
def get_total_approved_by_field(field: str):
    educations_by_field = [item for item in data if item.utbildningsomrade == field]
    
    if not educations_by_field:
        raise HTTPException(404, detail=f"Inget utbildningsområde hittades med namnet: {field}")

    total_sokta_platser = sum(item.sokta_platser_totalt for item in educations_by_field)
    total_beviljade_platser = sum(item.beviljade_platser_totalt for item in educations_by_field if item.beslut == "Beviljad")
    
    if total_sokta_platser > 0:
        approval_rate = (total_beviljade_platser / total_sokta_platser) * 100
    else:
        approval_rate = 0 # Sätt till 0 om inga platser söktes

    return {
        "Utbildningsomrade": field,
        "Totalt sökta platser": total_sokta_platser,
        "Total beviljade platser": total_beviljade_platser,
        "Beviljandegrad i %": round(approval_rate, 2)
    }