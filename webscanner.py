import asyncio
import aiohttp
from urllib.parse import urlparse

COMMON_PATHS = [
    "/admin", "/login", "/wp-admin", "/administrator",
    "/.env", "/.git/HEAD", "/config.php", "/config.json",
    "/database.sql", "/backup.zip", "/robots.txt", "/phpinfo.php"
]

WORDPRESS_PATHS = {
    "WordPress API (Users)": "/wp-json/wp/v2/users",
    "Information Readme File": "/readme.html",
    "License File": "/license.txt",
    "Login Page (Built-in)": "/wp-login.php",
    "Uploads Directory": "/wp-content/uploads/",
    "Yoast SEO Config (If active)": "/wp-json/yoast/v1/config",
}

SECURITY_HEADERS = {
    "Content-Security-Policy": "Protects against XSS attacks (malicious code injection).",
    "X-Frame-Options": "Protects against Clickjacking (embedding site into malicious frames).",
    "X-Content-Type-Options": "Prevents the browser from MIME-sniffing vulnerabilities.",
    "Strict-Transport-Security": "Enforces secure HTTPS connections (HSTS).",
    "Referrer-Policy": "Controls how much referrer information is passed on metadata."
}

CMS_MARKERS = {
    "WordPress": ["/wp-includes/", "/wp-content/", "wp-submit.php"]
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

async def scan_path(session, target_url, path, label=""):
    url = f"{target_url.rstrip('/')}{path}"
    try:
        async with session.get(url, headers=HEADERS, timeout=5, allow_redirects=False) as response:
            if response.status == 200:
                prefix = f"[WP-{label}]" if label else "[FOUND]"
                print(f"{prefix}: {url} -> Accessible (200 OK).")

                if "v2/users" in path:
                    try:
                        users_data = await response.json()
                        print("   [OSINT: Enumerated Site Users]:")
                        for user in users_data:
                            print(f"      - Username: {user.get('slug')} (Name: {user.get('name')})")
                    except Exception:
                        pass
            elif response.status == 403:
                prefix = f"[WP-{label}]" if label else "[RESTRICTED]"
                print(f"{prefix}: {url} -> Access Denied (403 Forbidden).")
    except Exception:
        pass

async def analyze_headers_and_tech(target_url):
    print(f"\n[*] Gathering general info and analyzing security configuration...")
    detected_cms = "Unknown"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(target_url, headers=HEADERS, timeout=7) as response:
                headers = response.headers
                html_text = await response.text()

                server = headers.get("Server", "Not specified (Hidden)")
                print(f"   [i] Web Server: {server}")

                for cms, markers in CMS_MARKERS.items():
                    if any(marker in html_text for marker in markers):
                        detected_cms = cms
                        break
                print(f"   [i] Detected CMS: {detected_cms}")

                print(f"\n[*] Auditing Security Headers:")
                missing_headers = 0
                for header, description in SECURITY_HEADERS.items():
                    if header in headers:
                        print(f"   [+] {header}: Present.")
                    else:
                        print(f"   [-] {header}: MISSING! {description}")
                        missing_headers += 1
                print(f"   [!] Status: {missing_headers} security headers are missing.")
    except Exception as e:
        print(f"[!] Analysis Error: {e}")
    return detected_cms

async def _async_main():
    target = input("Enter target URL for pentesting: ").strip()
    if not target.startswith("http://") and not target.startswith("https://"):
        target = "https://" + target

    parsed_url = urlparse(target)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    print(f"\n[*] Target Host: {base_url}")

    cms = await analyze_headers_and_tech(base_url)

    async with aiohttp.ClientSession() as session:
        print(f"\n[*] Launching asynchronous directory fuzzing ({len(COMMON_PATHS)} requests)...")
        tasks = [scan_path(session, base_url, path) for path in COMMON_PATHS]
        await asyncio.gather(*tasks)

        if cms == "WordPress":
            print(f"\n[!] WordPress engine detected! Activating specialized recon module ({len(WORDPRESS_PATHS)} requests)...")
            wp_tasks = [scan_path(session, base_url, path, label="RECON") for label, path in WORDPRESS_PATHS.items()]
            await asyncio.gather(*wp_tasks)

    print("\n[!] Scan process completely finished.")
    input("Press Enter to exit...")

def webscanner():
    asyncio.run(_async_main())

if __name__ == "__main__":
    webscanner()
