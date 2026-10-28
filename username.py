import asyncio
from urllib.parse import quote
import aiohttp

SITES = {
    "GitHub": {"url": "https://github.com/{}", "type": "status"},
    "Telegram": {"url": "https://t.me/{}", "type": "text_contains", "body_check": "tgme_page_extra"},
    "Reddit": {"url": "https://www.reddit.com/user/{}", "type": "status"},
    "Youtube": {"url": "https://www.youtube.com/@{}", "type": "status"},
    "Tryhackme": {"url": "https://tryhackme.com/p/{}", "type": "status"},
    "Fiverr": {"url": "https://www.fiverr.com/{}", "type": "status"},
    "Chess": {"url": "https://www.chess.com/member/{}", "type": "status"},
    "Snapchat": {"url": "https://www.snapchat.com/add/{}", "type": "status"},
    "Twitch": {"url": "https://www.twitch.tv/{}", "type": "status"},
    "Freelancer": {"url": "https://www.freelancer.com/u/{}", "type": "status"},
    "Codecademy": {"url": "https://www.codecademy.com/profiles/{}", "type": "status"},
    "Habr (Q&A)": {"url": "https://qna.habr.com/user/{}", "type": "status"},
    "Scratch": {"url": "https://scratch.mit.edu/users/{}", "type": "status"},
    "Donation Alerts": {"url": "https://www.donationalerts.com/r/{}", "type": "status"},
    "Patreon": {"url": "https://www.patreon.com/{}", "type": "status"},
    "Xbox Gamertag": {"url": "https://www.xboxgamertag.com/search/{}", "type": "status"},
    "Imgur": {"url": "https://imgur.com/user/{}/about", "type": "status"},
    "35photo": {"url": "https://35photo.pro/@{}", "type": "status"},
    "Boosty": {"url": "https://boosty.to/{}", "type": "status"},
    "Figma": {"url": "https://www.figma.com/@{}", "type": "status"},
    "Steam": {"url": "https://steamcommunity.com/id/{}", "type": "text_absent",
              "error_text": "The specified profile could not be found"},
    "Duolingo": {"url": "https://www.duolingo.com/profile/{}", "type": "status"},
    "Tenor": {"url": "https://tenor.com/users/{}", "type": "status"},
    "Freelance.ua": {"url": "https://freelance.ua/user/{}", "type": "status"},
    "Habr (User)": {"url": "https://habr.com/ru/users/{}", "type": "status"},
    "FACEIT": {"url": "https://www.faceit.com/en/players/{}", "type": "status"},
    "Pinterest": {"url": "https://www.pinterest.com/{}", "type": "status"},
    "Teletype": {"url": "https://teletype.in/@{}", "type": "status"},
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}


async def check_site(session, sem, name, data, username):
    url = data["url"].format(quote(username, safe=""))
    async with sem:
        try:
            async with session.get(url, allow_redirects=True) as resp:
                if resp.status != 200 or "login" in str(resp.url).lower():
                    return name, url, "not_found"

                kind = data["type"]
                if kind == "status":
                    return name, url, "found"

                text = await resp.text()
                if kind == "text_contains":
                    return name, url, "found" if data["body_check"] in text else "not_found"
                if kind == "text_absent":
                    return name, url, "not_found" if data["error_text"] in text else "found"
                return name, url, "not_found"
        except asyncio.TimeoutError:
            return name, url, "error: timeout"
        except aiohttp.ClientError as e:
            return name, url, f"error: {type(e).__name__}"


async def run(username):
    timeout = aiohttp.ClientTimeout(total=8)
    sem = asyncio.Semaphore(10)
    async with aiohttp.ClientSession(headers=HEADERS, timeout=timeout) as session:
        tasks = [check_site(session, sem, n, d, username) for n, d in SITES.items()]
        return await asyncio.gather(*tasks)


def username_tracker():
    username = input("Enter the username to search: ").strip()
    if not username:
        print("Username cannot be empty!")
        return

    print(f"\n[*] Searching for: {username}...\n")
    results = asyncio.run(run(username))

    found = [(n, u) for n, u, s in results if s == "found"]
    errors = [(n, s) for n, _, s in results if s.startswith("error")]

    for n, u in sorted(found):
        print(f"[+] {n}: {u}")
    for n, s in sorted(errors):
        print(f"[!] {n}: {s}")

    print(f"\n[!] Done. Found: {len(found)}, errors: {len(errors)}, "
          f"sites checked: {len(results)}.")
    input("Press Enter to exit -> ")


if __name__ == "__main__":
    username_tracker()
