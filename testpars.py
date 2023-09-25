import aiohttp
import asyncio


headers = {
        'User-Agent'    : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.1.800 Yowser/2.5 Safari/537.36',
        'Content-Type' : 'application/json',
    }



url = 'https://www.python.org/'
nums = range(5)

async def make_one_request(session, num):
	async with session.get(url) as response:
		return await response

async def make_many_requests(session):
	return await asyncio.gather(*[make_one_request(session, num) for num in nums])


def parse():
	session = aiohttp.ClientSession()
	tasks = make_many_requests(session)
	data = asyncio.run(tasks)
	
	print(data)
	



if __name__ == '__main__':
    parse()