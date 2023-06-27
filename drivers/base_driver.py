from typing import Optional


class BaseDriver:
    NAME = "_"
    REQUIRED_ARGS = []

    async def setup(self):
        pass

    async def create_url(self, url: str, name: Optional[str] = None) -> Optional[str]:
        raise NotImplementedError("Not Implemented")

    async def get_url(self, name: str) -> Optional[str]:
        raise NotImplementedError("Not Implemented")
