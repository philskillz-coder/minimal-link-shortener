import json
import os.path
from drivers.base import BaseDriver
from hashids import Hashids
import aiofiles
from typing import Optional


class Driver(BaseDriver):
    NAME = "json"
    REQUIRED_ARGS = [
        {
            "name": "file",
            "display": "File",
            "description": "file for the json storage file",
            "type": str,
            "required": True,
            "default": "data/data.json"
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

    # noinspection PyTypeChecker
    def __init__(self, file: str, length: int, secret: str, alphabet: str):
        self.file = file

        self.hashids = Hashids(secret, length, alphabet)

        # in setup
        self.urls: list = None
        self.counter: int = None

    async def setup(self):
        # create data file if not exists
        if not os.path.isfile(self.file):
            os.makedirs(self.file, exist_ok=True)
            self.urls = []
            self.counter = 0
        else:
            async with aiofiles.open(self.file, "rb") as f:
                self.urls = json.loads((await f.read()).decode())
                self.counter = len(self.urls)

    async def create_url(self, url: str) -> str:
        name = self.hashids.encode(self.counter)
        self.counter += 1
        self.urls.append(url)

        async with aiofiles.open(self.file, "wb") as f:
            await f.write(json.dumps(self.urls, indent=4))

        return name

    async def get_url(self, name: str) -> Optional[str]:
        decoded = self.hashids.decode(name)
        if not decoded:
            return None
        return decoded[0]
