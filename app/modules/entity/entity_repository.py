from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .entity_model import Entity

class EntityRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, entity: Entity) -> Entity:
        self.session.add(entity)
        await self.session.flush()  # Generate ID
        await self.session.refresh(entity)  # Refresh object with new ID
        return entity

    async def get_all(self):
        result = await self.session.execute(select(Entity))
        return result.scalars().all()
