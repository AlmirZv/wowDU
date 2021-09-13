from gino import Gino
from gino.schema import GinoSchemaVisitor

from data.config import POSTGRESURI

db_gino = Gino()

async def create_db():
    await db_gino.set_bind(POSTGRESURI)
    db_gino.gino: GinoSchemaVisitor
    await db_gino.gino.create_all()