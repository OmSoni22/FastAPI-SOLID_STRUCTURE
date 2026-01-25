from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, Type, TypeVar

from app.modules.notification.services.notification_service import NotificationService
from app.modules.entity.services.entity_service import EntityService

class ServiceFactory:
    """
    Factory to manage service instantiation and dependency injection.
    Scope: Per Request.
    """
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self._services: Dict[str, Any] = {}

    @property
    def notification(self) -> NotificationService:
        """Get or create NotificationService."""
        if "notification" not in self._services:
            self._services["notification"] = NotificationService()
        return self._services["notification"]

    @property
    def entity(self) -> EntityService:
        """Get or create EntityService with dependencies."""
        if "entity" not in self._services:
            # Auto-wire dependencies: EntityService needs Session + NotificationService
            self._services["entity"] = EntityService(
                session=self.session, 
                notification_service=self.notification
            )
        return self._services["entity"]
