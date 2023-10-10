from fastapi import APIRouter
from pydantic import BaseModel
from scrapers.trekomania import TrekomaniaScrapper
from multiprocessing import Process
from scrapers.trekomania import TrekomaniaScrapper

router = APIRouter(prefix="/scraper")

def run_scraper():
    scraper = TrekomaniaScrapper()
    scraper.run()

@router.post('/trekomaniaScraper')
def start_trekomania_scraper():
    # Create a new process to run the scraper
    process = Process(target=run_scraper)
    process.start()
    
    return {"message": "Trekomania scraper execution started successfully."}