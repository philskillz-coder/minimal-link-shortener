from typing import Optional

from drivers.base import BaseDriver
import sqlite3

class Driver(BaseDriver):
    REQUIRED_ARGS = [
        {
            "name": "file",
            "display": "File",
            "description": "The sqlite database file",
            "type": str,
            "required": True,
            "default": "data/data.sqlite"
        }
    ]
    NAME = "sqlite"

    async def setup(self):
        pass

    async def create_url(self, url: str):
        raise NotImplementedError("Not Implemented")

    async def get_url(self, name: str) -> Optional[str]:
        raise NotImplementedError("Not Implemented")
