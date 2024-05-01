import aiohttp
import asyncio
import sys
from datetime import datetime, timedelta


async def fetch_exchange_rate(date):
    async with aiohttp.ClientSession() as session:
        url = f'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5&date={date.strftime("%d.%m.%Y")}'
        async with session.get(url) as response:
            result = await response.json()
            return result


async def main():
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <days>")
        return

    try:
        days = int(sys.argv[1])
        if days > 10:
            print("Too many days, more then 10 days not supported")
            return
    except ValueError:
        print("Invalid input. Please enter a valid number of days.")
        return

    dates = [datetime.now() - timedelta(days=i) for i in range(1, days + 1)]
    tasks = [fetch_exchange_rate(date) for date in dates]
    results = await asyncio.gather(*tasks)

    return results


if __name__ == "__main__":
    results = asyncio.run(main())

    for i, result in enumerate(results, 1):
        print(f"Exchange rate for {datetime.now() - timedelta(days=i)}:")
        print(result)
        print()