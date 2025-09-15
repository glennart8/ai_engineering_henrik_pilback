from fastapi import FastAPI, APIRouter
from data_processing import DataExplorer


#Skapar en instans av FastAPI och router
app = FastAPI()
router = APIRouter(prefix="/api/sales") # För att slippa använda långa end-points

# RETURNERA HELA JSON-RESULTATET
@app.get("/")
async def read_sales():
    data_explorer = DataExplorer()
    return data_explorer.json_response()


@router.get("/summary")
async def read_summary_data():
    data_explorer = DataExplorer()
    return data_explorer.summary().json_response()


@router.get("/kpis")
async def read_kpis(country: str):
    """ KPIs based on country"""
    data_explorer = DataExplorer()
    return data_explorer.kpis(country=country)

app.include_router(router)