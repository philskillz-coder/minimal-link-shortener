from typing import Optional
from hashids import Hashids
from drivers.base_driver import BaseDriver
import aiosqlite


# sqlite.py

# noinspection PyTypeChecker
class Driver(BaseDriver):
    REQUIRED_ARGS = [
        {
            "name": "file",
            "display": "File",
            "description": "The sqlite database file",
            "type": str,
            "required": True,
            "default": "data/data.sqlite"
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
    NAME = "sqlite"

    __table__ = "CREATE TABLE IF NOT EXISTS \"urls\" (\"id\" INTEGER NOT NULL UNIQUE, name TEXT UNIQUE, \"url\" TEXT NOT NULL, " \
                "PRIMARY KEY(\"id\" AUTOINCREMENT))"

    def __init__(self, file: str, length: int, secret: str, alphabet: str):
        self.file = file
        self.hashids = Hashids(secret, length, alphabet)
        # noinspection PyTypeChecker
        self.connection: aiosqlite.Connection = None

    async def setup(self):
        self.connection: aiosqlite.Connection = await aiosqlite.connect(self.file)
        await self.connection.execute(self.__table__)

    async def create_url(self, url: str, name: Optional[str] = None) -> Optional[str]:
        if name is not None:
            async with self.connection.execute("SELECT EXISTS(SELECT 1 FROM urls WHERE name = ?)", (name,)) as cursor:
                exists, = await cursor.fetchone()
                if not exists:
                    await cursor.execute("INSERT INTO urls(name, url) VALUES(?, ?)", (name, url))
                    return name
                return None
        async with self.connection.execute("INSERT INTO urls(url) VALUES(?)", (url,)) as cursor:
            _id = cursor.lastrowid

        await self.connection.commit()
        return self.hashids.encode(_id)

    async def get_url(self, name: str) -> Optional[str]:
        async with self.connection.execute("SELECT url FROM urls WHERE name = ?", (name,)) as cursor:
            url = await cursor.fetchone()
            if url is not None:
                return url[0]

            decoded = self.hashids.decode(name)
            if not decoded:
                return None

            await cursor.execute("SELECT url FROM urls WHERE id = ?", (decoded[0],))

            url = await cursor.fetchone()
            return None if url is None else url[0]
