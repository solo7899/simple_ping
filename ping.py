import argparse
import asyncio
import httpx


def parse_args():
    parser = argparse.ArgumentParser(description=" Ping one or multiple URL(s) and get the average response time for each website")
    parser.add_argument("url", help="URL(s) to ping; seperate multiple URLs with a comma")
    
    return parser.parse_args()

async def get_ping(client: httpx.AsyncClient, url:str):
    print(f"[*] Pinging {url}...")
    response = await  client.get(url, follow_redirects=True)
    response.raise_for_status()

    return response.url, response.elapsed

async def main():
    args = parse_args()
    async with httpx.AsyncClient() as client:
        async with asyncio.TaskGroup() as tg:
            tasks = {url:[tg.create_task(get_ping(client, url)) for _ in range(3)] for url in args.url.split(",")}
        for task in tasks:
            url, elapsed = task.result()
            print(url, ":", elapsed)

#todo : get muliple urls from command line arguments

if __name__ == "__main__":
    asyncio.run(main())
