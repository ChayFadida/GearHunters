from fastapi import APIRouter, Depends
from pydantic import BaseModel
from scrapers.trekomania import TrekomaniaScrapper
from multiprocessing import Process
from scrapers.trekomania import TrekomaniaScrapper
from router.authorization import is_admin

router = APIRouter(prefix="/scraper")

def run_scraper():
    scraper = TrekomaniaScrapper()
    scraper.run()

@router.post('/trekomaniaScraper', tags=["admin"])
def start_trekomania_scraper(current_user: dict = Depends(is_admin)):
    # Create a new process to run the scraper
    process = Process(target=run_scraper)
    process.start()
    
    return {"message": "Trekomania scraper execution started successfully."}