from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Pokemon

async def get_pokemons(db: AsyncSession, name: str = None, type: str = None):
    query = select(Pokemon)
    if name:
        query = query.where(Pokemon.name.ilike(f"%{name}%"))
    if type:
        query = query.where(Pokemon.type.ilike(f"%{type}%"))
    result = await db.execute(query)
    return result.scalars().all()

async def create_pokemon(db: AsyncSession, name: str, image_url: str, type: str):
    db_pokemon = Pokemon(name=name, image_url=image_url, type=type)
    db.add(db_pokemon)
    await db.commit()
    await db.refresh(db_pokemon)
    return db_pokemon
