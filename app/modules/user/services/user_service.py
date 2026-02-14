from sqlalchemy.ext.asyncio import AsyncSession
from ..user_repository import UserRepository
from ..user_model import User
from ..user_schema import UserCreate
# Note: We don't import NotificationService type here to avoid circular imports if it ever happens? 
# Actually we can import checking TYPE_CHECKING or just import if distinct.
from app.modules.notification.services.notification_service import NotificationService

class UserService:
    def __init__(self, session: AsyncSession, notification_service: NotificationService):
        self.repository = UserRepository(session)
        self.notification_service = notification_service

    async def create_user(self, payload: UserCreate) -> User:
        user = User(**payload.model_dump())
        created_user = await self.repository.create(user)
        
        # Send notification
        await self.notification_service.send_email(
            recipient="admin@example.com",
            subject="New User Created",
            body=f"User '{created_user.name}' was created with ID {created_user.id}"
        )
        
        return created_user

    async def get_users(self):
