from sqlalchemy.ext.asyncio import AsyncSession
from ..entity_repository import EntityRepository
from ..entity_model import Entity
from ..entity_schema import EntityCreate
# Note: We don't import NotificationService type here to avoid circular imports if it ever happens? 
# Actually we can import checking TYPE_CHECKING or just import if distinct.
from app.modules.notification.services.notification_service import NotificationService

class EntityService:
    def __init__(self, session: AsyncSession, notification_service: NotificationService):
        self.repository = EntityRepository(session)
        self.notification_service = notification_service

    async def create_entity(self, payload: EntityCreate) -> Entity:
        entity = Entity(**payload.model_dump())
        created_entity = await self.repository.create(entity)
        
        # Send notification
        await self.notification_service.send_email(
            recipient="admin@example.com",
            subject="New Entity Created",
            body=f"Entity '{created_entity.name}' was created with ID {created_entity.id}"
        )
        
        return created_entity

    async def get_entities(self):
        return await self.repository.get_all()
