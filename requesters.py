from abc import ABC, abstractmethod
import json
import asyncio


class AsyncRequester(ABC):

    @staticmethod
    async def decode_responce(response):
        try:
            json_data = await response.json(content_type='text/html')
        except json.JSONDecodeError as e:
            json_data = None
        html_data = await response.text() 
        status_code = response.status 
        return {
            'status' : status_code,
            'html' : html_data,
            'json' : json_data
        }

    @abstractmethod
    async def make_request(self, url, body):
        pass

class AsyncPostRequester(AsyncRequester):
    async def make_request(self, url, body, session):
        response = await session.post(url, data=body)
        return await self.decode_responce(response)

class AsyncGetRequester(AsyncRequester):
    async def make_request(self, url, body, session):
        response = await session.get(url, data=body)
        return await self.decode_responce(response)
