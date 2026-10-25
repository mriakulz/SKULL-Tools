import requests

def username():

    username = input("write the username: ")

    sites = {
        "GitHub": "https://github.com/{}",
        "Twitter": "https://twitter.com/{}",
        "Instagram": "https://www.instagram.com/{}/",
        "Reddit": "https://www.reddit.com/user/{}",
        "Youtube": "https://www.youtube.com/{}",
        "Tryhackme": "https://tryhackme.com/{}",
        "Fiverr": "https://www.fiverr.com/{}",
        "Chess": "https://www.chess.com/member/{}",
        "Snapchat": "https://www.snapchat.com/add/{}",
        "Tiktok": "https://www.tiktok.com/@{}",
        "Twitch": "https://www.twitch.tv/{}",
        "Linkedin": "https://www.linkedin.com/in/{}",
        "Freelancer": "https://www.freelancer.com/u/{}",
        "Codecademy": "https://www.codecademy.com/profiles/{}",
        "Habr (Q&A)": "https://qna.habr.com/user/{}",
        "Scratch": "https://scratch.mit.edu/users/{}",
        "Donation Alerts": "https://www.donationalerts.com/r/{}",
        "Patreon": "https://www.patreon.com/{}",
        "Diablo": "https://www.habbo.com.tr/profile/{}",
        "Xbox Gamertag": "https://www.xboxgamertag.com/search/{}",
        "Imgur": "https://imgur.com/user/{}/about",
        "35photo": "https://35photo.pro/@{}",
        "7dach": "https://7dach.ru/profile/{}",
        "Boosty": "https://boosty.to/{}",
        "Figma": "https://www.figma.com/@{}",
        "Picsart": "https://picsart.com/u/{}",
        "Tinder": "https://tinder.com/@{}",
        "Plink": "https://plink.gg/user/{}",
        "Steam": "https://steamcommunity.com/id/{}",
        "Duolingo": "https://www.duolingo.com/profile/{}",
        "Tenor": "https://tenor.com/users/{}",
        "Spotify": "https://open.spotify.com/user/{}",
        "Discord (Invite)": "https://discord.com/invite/{}",
        "Freelance.ua": "https://freelance.ua/user/{}",
        "Habr (User)": "https://habr.com/ru/users/{}",
        "Telegram": "https://t.me/{}",
        "FACEIT": "https://www.faceit.com/en/players/{}",
        "Pinterest": "https://www.pinterest.com/{}",
        "Dating.ru": "https://dating.ru/{}",
        "Facebook": "https://www.facebook.com/{}",
        "Teletype": "https://teletype.in/@{}"
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    def check_username(username):
        for name, url in sites.items():
            full_url = url.format(username)
            try:
                response = requests.get(full_url, headers=headers, timeout=5)
                if response.status_code == 200:
                    print(f"[+] {name}: ({full_url})")
                #elif response.status_code == 404:
                    #print(f"[-] {name}: -")
                #else:
                    #print(f"[?] {name}: CODE {response.status_code}")

            except requests.exceptions.RequestException:
                print(f"[!] {name}: ERROR")

    check_username(username)

    input(" [!] | Press to continue -> ")
