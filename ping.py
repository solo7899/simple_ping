import asyncio
import httpx
import sys


async def get_ping(client: httpx.AsyncClient, url:str):
    print(f"[*] Pinging {url}...")
    response = await  client.get(url, follow_redirects=True)
    response.raise_for_status()

    return response.url, response.elapsed


async def main():
    url = "https://google.com"
    async with httpx.AsyncClient() as client:
        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(get_ping(client, url)) for _ in range(3)]
        for task in tasks:
            url, elapsed = task.result()
            print(url, ":", elapsed)


if __name__ == "__main__":
    asyncio.run(main())
