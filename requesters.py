from abc import ABC, abstractmethod


class AsyncRequester(ABC):
    def __init__(self, session):
        self.session = session

    @abstractmethod
    async def make_request(self, url, body):
        pass

class AsyncPostRequester(AsyncRequester):
    async def make_request(self, url, body):
        async with self.session().post(url, data=body) as response:        
            return await response

class AsyncGetRequester(AsyncRequester):
    async def make_request(self, url, body):
        async with self.session().get(url, data=body) as response:        
            return await response
