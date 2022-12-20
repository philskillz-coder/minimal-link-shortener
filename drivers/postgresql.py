from typing import Optional

from hashids import Hashids

from drivers.base import BaseDriver
import asyncpg


# noinspection PyTypeChecker
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

    __table__ = "CREATE TABLE IF NOT EXISTS urls (id SERIAL PRIMARY KEY NOT NULL UNIQUE, name TEXT UNIQUE, url TEXT NOT NULL);"

    def __init__(self, host: str, port: int, database: str, user: str, password: str, length: int, secret: str,
                 alphabet: str):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.hashids = Hashids(secret, length, alphabet)
        self.connection: asyncpg.Connection = None

    async def setup(self):
        self.connection: asyncpg.Connection = await asyncpg.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            database=self.database,
            password=self.password
        )
        await self.connection.execute(self.__table__)

    async def create_url(self, url: str, name: Optional[str] = None) -> Optional[str]:
        if name is not None:
            exists, = await self.connection.fetchrow("SELECT EXISTS(SELECT 1 FROM urls WHERE name = $1)", name)
            if exists:
                return None
            await self.connection.execute("INSERT INTO urls(name, url) VALUES($1, $2)", name, url)
            return name
        else:
            _id, = await self.connection.fetchrow("INSERT INTO urls(url) VALUES($1) RETURNING id;", url)
            return self.hashids.encode(_id)

    async def get_url(self, name: str) -> Optional[str]:
        exists, = await self.connection.fetchrow("SELECT EXISTS(SELECT 1 FROM urls WHERE name = $1)", name)
        if exists:
            target, = await self.connection.fetchrow("SELECT url FROM urls WHERE name = $1", name)
            return target

        decoded = self.hashids.decode(name)
        if not decoded:
            return None

        url = await self.connection.fetchrow("SELECT url FROM urls WHERE id = $1", decoded)
        if url is None:
            return None

        return url[0]
