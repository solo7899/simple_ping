import argparse
import asyncio
import httpx


def parse_args():
    parser = argparse.ArgumentParser(description=" Ping one or multiple URL(s) and get the average response time for each website")
    parser.add_argument("url", help="URL(s) to ping; seperate multiple URLs with a comma")
    
    return parser.parse_args()

async def get_ping(client: httpx.AsyncClient, url:str):
    try:
        response = await  client.get(url if url.startswith("http") else f"http://{url}", follow_redirects=True)
        response.raise_for_status()
        return response.elapsed.total_seconds()
    except httpx.HTTPStatusError as e: 
        print(f"Error for {url}: {e}")
        return None

def get_average_time(*times):
    valid_times = [t for t in times if t is not None]
    if not valid_times:
        return None
    return sum(valid_times) / len(valid_times)

async def main():
    args = parse_args()

    async with httpx.AsyncClient() as client:
        async with asyncio.TaskGroup() as tg:
            tasks_lists = {url.strip():[tg.create_task(get_ping(client, url)) for _ in range(3)] for url in args.url.split(",")}
        for url, tasks in tasks_lists.items():
                elapseds = map(lambda t: t.result(), tasks)
                tasks_lists[url] =  elapseds 

    for url, elapseds in tasks_lists.items():
        average = get_average_time(*elapseds)
        if average is None: 
            print(f"{url:<15}: All request failed")
        else:
            print(f"{url:<15} : {average:.2f} second(s)")

if __name__ == "__main__":
    asyncio.run(main())
