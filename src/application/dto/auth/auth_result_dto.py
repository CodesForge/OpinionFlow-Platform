from dataclasses import dataclass

@dataclass(frozen=True)
class AuthResultDto:
    status: str
    message: str
    access_token: str