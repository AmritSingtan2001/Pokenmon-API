import asyncio
import httpx
from fastapi import FastAPI, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import SessionLocal, init_db
from app.crud import create_pokemon, get_pokemons
from app.schemas import Pokemon

app = FastAPI()

async def get_db():
    async with SessionLocal() as session:
        yield session

@app.on_event("startup")
async def startup_event():
    await init_db()
    async with httpx.AsyncClient() as client:
        response = await client.get("https://pokeapi.co/api/v2/pokemon?limit=151")
        pokemons = response.json()["results"]
        for pokemon in pokemons:
            poke_data = await client.get(pokemon["url"])
            poke_json = poke_data.json()
            await create_pokemon(
                db=next(get_db()), 
                name=poke_json["name"], 
                image_url=poke_json["sprites"]["front_default"],
                type=poke_json["types"][0]["type"]["name"]
            )

@app.get("/api/v1/pokemons", response_model=list[Pokemon])
async def read_pokemons(name: str = Query(None), type: str = Query(None), db: AsyncSession = Depends(get_db)):
    pokemons = await get_pokemons(db, name, type)
    return pokemons
