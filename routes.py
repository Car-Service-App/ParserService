from fastapi import APIRouter

from router import ozon_parser_router

routes = APIRouter()

routes.include_router(ozon_parser_router.ozon_parser_router, prefix="/ozon")
