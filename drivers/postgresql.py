from typing import Optional

from drivers.base import BaseDriver
import asyncpg


class Driver(BaseDriver):
    NAME = "postgresql"
    REQUIRED_ARGS = [
        {
            "name": "host",
            "display": "Host",
            "description": "Postgresql host",
            "type": str,
            "required": True,
            "default": "localhost"
        },
        {
            "name": "port",
            "display": "Port",
            "description": "Postgresql port",
            "type": int,
            "required": True,
            "default": "5432"
        },
        {
            "name": "database",
            "display": "Database",
            "description": "Which database to use",
            "type": str,
            "required": True
        },
        {
            "name": "user",
            "display": "User",
            "description": "Postgres user",
            "type": str,
            "required": True
        },
        {
            "name": "password",
            "display": "Password",
            "description": "Postgres user password",
            "type": str,
            "required": True
        },
        {
            "name": "length",
            "display": "Length",
            "description": "minimal link length",
            "type": int,
            "required": True,
            "default": 5
        },
        {
            "name": "secret",
            "display": "Secret",
            "description": "link secret",
            "type": str,
            "required": True
        },
        {
            "name": "alphabet",
            "display": "Alphabet",
            "description": "which letters to use in links",
            "type": str,
            "required": True,
            "default": "abcdefghijklmnopqrstuvwxyz"
        }
    ]

    def __init__(self, host: str, port: int, database: str, user: str, password: str, length: int, secret: str,
                 alphabet: str):
        pass

    async def setup(self):
        pass

    async def create_url(self, url: str):
        raise NotImplementedError("Not Implemented")

    async def get_url(self, name: str) -> Optional[str]:
        raise NotImplementedError("Not Implemented")
