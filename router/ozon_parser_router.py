from fastapi import APIRouter

from schema.extra_schema import Message
from service.ozon_parser import CarPartScraper

ozon_parser_router = APIRouter(
    tags=['parser']
)


@ozon_parser_router.get('/scrap/{search}', responses={400: {'dto': Message}})
async def get_parsed_ozon(search: str):
    scraper = CarPartScraper(search)
    car_parts = scraper.run()
    return car_parts
