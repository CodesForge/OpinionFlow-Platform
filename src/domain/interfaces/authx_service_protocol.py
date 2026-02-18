from typing import Protocol

class AuthxServiceProtocol(Protocol):
    async def create_access_token(self, uid: str) -> str: ...