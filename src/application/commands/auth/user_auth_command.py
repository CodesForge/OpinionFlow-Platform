from dataclasses import dataclass

@dataclass(frozen=True)
class UserAuthCommand:
    username: str
    password: str