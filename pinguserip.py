import sys
import os
import subprocess
import re
import requests
import socket
import ssl
import os
sys.stdout.reconfigure(encoding='utf-8')


def pinguserip():

    def clear_screen():
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def geo_info(ip):
        url = f"http://ip-api.com/json/{ip}"
        response = requests.get(url, timeout=5)
        return response.json()

    def reverse_dns(ip):
        try:
            return socket.gethostbyaddr(ip)[0]
        except socket.herror:
            return None

    def pinguserip(ip):
        result = subprocess.run(
            f"ping {ip} -n 2",
            shell=True,
            capture_output=True,
            text=True
        )
        return result.stdout

        match = re.search(r"Average = (\d+)ms", result.stdout)
        return match.group(1) + " ms" if match else "unknown"

    ip = input("targer ip user:")

    print(f"IP: {ip}")

    geo = geo_info(ip)

    print("\n--- Geo Info ---")
    print("country:", geo.get("country"))
    print("region:", geo.get("regionName"))
    print("city:", geo.get("city"))
    print("timezone:", geo.get("timezone"))

    print("\n--- Provider ---")
    print("ISP:", geo.get("isp"))
    print("Organization:", geo.get("org"))
    print("ASN:", geo.get("as"))

    print("\n--- Network ---")
    print("Тип IP:", "Mobile" if geo.get("mobile") else "Home / Other")
    print("Proxy / VPN:", geo.get("proxy"))

    print("\n--- Reverse DNS ---")
    print(reverse_dns(ip))

    print("\n--- Ping ---")
    print(pinguserip(ip))
    input(" [!] | Press to continue -> ")
