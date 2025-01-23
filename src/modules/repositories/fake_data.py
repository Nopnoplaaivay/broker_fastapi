from src.db.sessions import backend_session_scope
from src.modules.base.repositories import BaseRepo
from src.modules.entities import FakeData

class FakeDataRepo(BaseRepo[FakeData]):
    entity = FakeData
    async_session_scope = backend_session_scope