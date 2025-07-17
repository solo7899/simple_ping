import argparse
import asyncio
import httpx


def parse_args():
    parser = argparse.ArgumentParser(description=" Ping one or multiple URL(s) and get the average response time for each website")
    parser.add_argument("url", help="URL(s) to ping; seperate multiple URLs with a comma")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode")
    parser.add_argument("-c", "--count", type=int, default=3, help="Number of pings per URL")
    
    return parser.parse_args()

async def get_ping(client: httpx.AsyncClient, url:str, verbose):
    try:
        response = await  client.get(url if url.startswith("http") else f"http://{url}", follow_redirects=True)
        if verbose:
            print(f"Response for {url:<15}: {response.status_code:<5} - {response.elapsed.total_seconds():<5.2f} seconds")
        response.raise_for_status()
        return response.elapsed.total_seconds()
    except httpx.HTTPStatusError as e: 
        if verbose:
            print(f"Error for {url}: {e}")
        return None
    except httpx.RequestError as e:
        if verbose:
            print(f"Error for {url}: {e}")
        return None

def get_average_time(*times):
    valid_times = [t for t in times if t is not None]
    if not valid_times:
        return None
    return sum(valid_times) / len(valid_times)

def display_output(tasks_lists):
    for url, elapseds in tasks_lists.items():
        average = get_average_time(*elapseds)
        if average is None: 
            print(f"{url:<15}: All request failed")
        else:
            print(f"{url:<15} : {average:.2f} second(s)")

async def main():
    args = parse_args()

    async with httpx.AsyncClient() as client:
        async with asyncio.TaskGroup() as tg:
            tasks_lists = {url.strip():[tg.create_task(get_ping(client, url, args.verbose)) for _ in range(args.count)] for url in args.url.split(",")}
        for url, tasks in tasks_lists.items():
                elapsed_times = map(lambda t: t.result(), tasks)
                tasks_lists[url] =  elapsed_times 

    display_output(tasks_lists)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
