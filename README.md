# 💀 SKULL

**SKULL** is a console toolkit of network and OSINT tools written in Python 3, with a simple text-based menu.

| | |
|---|---|
| **Version** | 1.11 |
| **Interface language** | English |
| **Written in** | Python 3 |
| **Platforms** | Windows 10/11, Linux (see [Known limitations](#known-limitations)) |
| **Author** | Mriakulz |
| **License** | [MIT](LICENSE) |

---

## Features

The program has a paged menu with three sections: **Network Scanner**, **Osint** and **Utilities**.

### Network Scanner

**`1` — Target Link.** Analyzes a domain (enter it without `https://`):

- resolves the domain to an IP address;
- pings the host (2 packets);
- geolocation info: country, city, ISP, organization, ASN;
- reverse DNS lookup;
- SSL certificate info: issuer, valid from / valid to.

**`2` — Target IP.** Analyzes an IP address you provide:

- geolocation info: country, region, city, timezone;
- provider info: ISP, organization, ASN;
- network type (mobile or home/other) and a Proxy / VPN flag;
- reverse DNS lookup;
- ping.

### Osint

**`7` — Username Tracker.** Checks whether a username exists on **41 websites** (GitHub, Reddit, Instagram, Telegram, Steam, TikTok, Twitch, Chess.com, Habr and more). Only found profiles (HTTP 200) are printed, with links; if a site can't be reached, `[!] <site>: ERROR` is shown.

**`8` — Phone Info.** Analyzes a phone number entered in international format (with `+`, e.g. `+380671234567`). Works offline, using the built-in prefix database of the `phonenumbers` library:

- number validation;
- international and national formats;
- country;
- region (available for landline numbers only);
- carrier;
- number type (mobile, landline, VoIP, toll-free);
- time zone.

**New Features:**
- **Global OSINT Web Lookup:** Automatically scans the internet using Google Custom Search API to find any public leaks, listings, or websites where the number is exposed (checks both international and clean national formats simultaneously).
- **US/Canada Toll-Free Country Fix:** Resolves a bug to correctly identify and output country names for North American toll-free ranges.
- **Fully Localized English Interface:** Complete translation of all inputs, outputs, and prompt messages into English for a clean, unified user experience.
- **Code Optimization:** Completely stripped of comments and unnecessary diagnostic logs for improved execution speed and clean terminal formatting.


> The remaining menu slots (3–6, 9+ and the whole second page) are reserved for future tools.

---

## Installation

```bash
git clone -b SKULL https://github.com/mriakulz/SKULL-Tools.git
cd SKULL-Tools
pip install colorama tqdm requests phonenumbers
```

### Dependencies

| Package | Purpose |
|---|---|
| `colorama` | colored terminal output |
| `tqdm` | progress bar on exit |
| `requests` | HTTP requests (geolocation, username checks) |
| `phonenumbers` | phone number parsing and info (tool 8) |

**Python 3** and an Internet connection are required (except for Phone Info, which works offline). The `socket`, `ssl` and `subprocess` modules are part of the standard library.

---

## Usage

Run from the project folder, because the menu state file `menu.txt` is read from the current directory:

```bash
python main.py
```

---

## Controls

| Key | Action |
|---|---|
| `1`, `2`, `7`, `8` | run the corresponding tool |
| `N` | next menu page |
| `B` | back to the previous menu page |
| `I` | program info |
| `Q` | quit |

The current menu page number is stored in `menu.txt`.

---

## Project structure

```
SKULL-Tools/
├── main.py         # main menu and entry point
├── pinglink.py     # tool 1: Target Link
├── pinguserip.py   # tool 2: Target IP
├── username.py     # tool 7: Username Tracker
├── phoneinfo.py    # tool 8: Phone Info
├── menu.txt        # current menu page number
└── LICENSE         # MIT
```

---

## Known limitations

- **Ping works on Windows only.** The code uses the `-n 2` flag; on Linux/macOS it should be `-c 2`, so the "Ping" section shows no result there. Everything else works on all platforms.
- **IP geolocation** comes from the free [ip-api.com](https://ip-api.com) service over HTTP, which is rate-limited; accuracy depends on the service and is often approximate.
- **Username Tracker** treats a profile as found when the response code is 200. Some sites (Instagram, Facebook, LinkedIn, TikTok, etc.) may block requests or return 200 for non-existent pages, so false positives and misses are possible. Verify results manually.
- **Phone Info** is based on number prefixes only. Mobile numbers are not tied to a region, so only the country is shown for them. The carrier is the one the number was originally issued by, so it can be outdated if the owner switched operators (number portability). The tool cannot identify the owner or the current location of a number.

---

## Disclaimer

This tool is intended for learning, auditing your own infrastructure and lawful collection of publicly available information. Use it only in compliance with applicable laws and the terms of the services involved. The author is not responsible for misuse.

---

## License

Released under the [MIT License](LICENSE) © 2026 Mriakulz.
