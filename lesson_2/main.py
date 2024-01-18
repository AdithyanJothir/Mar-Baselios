import time
import asyncio
from fastapi import FastAPI
import httpx
from pydantic import BaseModel


app = FastAPI()


class Country(BaseModel):
    name: str
    official_name: str


@app.get("/sync")
def sync_route():
    time.sleep(2)
    return {"message": "This is a synchronous route"}


@app.get("/async")
async def async_route():
    await asyncio.sleep(2)
    return {"message": "This is an asynchronous route"}


@app.get("/countries")
async def get_countries():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://restcountries.com/v3.1/all")
        countries = response.json()

        countries = countries[:100]

        countries_base_models: list[Country] = []
        for country in countries:
            country_base_model = Country(
                name=country["name"]["common"],
                official_name=country["name"]["official"],
            )

            countries_base_models.append(country_base_model)
        return countries_base_models
