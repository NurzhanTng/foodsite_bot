import aiohttp
from aiogram import Bot

from core.settings import settings


class RestHandler:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.basic_url = settings.bots.api_path
        self.basic_headers = {
            'Content-Type': 'application/json',
        }

    async def get(self, url: str, params: dict = None, headers: dict = None):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.basic_url + url, params=params, headers=headers) as response:
                # print("Response", response)
                return await response.json()

    async def post(self, url: str, data: dict = None, headers: dict = None):
        if headers is None:
            headers = self.basic_headers
        else:
            headers = {**self.basic_headers, **headers}

        async with aiohttp.ClientSession() as session:
            async with session.post(self.basic_url + url, json=data, headers=headers) as response:
                return await response.json()

    async def update(self, url: str, data: dict = None, headers: dict = None):
        if headers is None:
            headers = self.basic_headers
        else:
            headers = {**self.basic_headers, **headers}

        async with aiohttp.ClientSession() as session:
            async with session.put(self.basic_url + url, json=data, headers=headers) as response:
                return await response.json()

    async def delete(self, url: str, headers: dict = None):
        async with aiohttp.ClientSession() as session:
            async with session.delete(self.basic_url + url, headers=headers) as response:
                return await response.json()
