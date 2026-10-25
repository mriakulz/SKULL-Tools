import sys
import subprocess
import requests
import socket
import ssl
import os
import main
sys.stdout.reconfigure(encoding='utf-8')


def pinglink():

    domain = input("write the link without https://:")

    def clear_screen():
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def get_ip(domain):
        return socket.gethostbyname(domain)

    def pinglink(ip):
        result = subprocess.run(
            f"ping {ip} -n 2",
            shell=True,
            capture_output=True,
            text=True
        )
        return result.stdout

    def geo_info(ip):
        url = f"http://ip-api.com/json/{ip}"
        return requests.get(url).json()

    def reverse_dns(ip):
        try:
            return socket.gethostbyaddr(ip)[0]
        except:
            return None

    def ssl_info(domain):
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(
            socket.socket(), server_hostname=domain
        ) as s:
            s.settimeout(5)
            s.connect((domain, 443))
            cert = s.getpeercert()

        return {
            "issuer": dict(x[0] for x in cert["issuer"]),
            "valid_from": cert["notBefore"],
            "valid_to": cert["notAfter"]
        }

    ip = get_ip(domain)
    print(f"IP: {ip}")

    print("\n--- Ping ---")
    print(pinglink(ip))

    print("--- Geo Info ---")
    geo = geo_info(ip)
    for k in ["country", "city", "isp", "org", "as"]:
        print(f"{k}: {geo.get(k)}")

    print("\n--- Reverse DNS ---")
    print(reverse_dns(ip))

    print("\n--- SSL ---")
    ssl_data = ssl_info(domain)
    print("Issuer:", ssl_data["issuer"])
    print("Valid from:", ssl_data["valid_from"])
    print("Valid to:", ssl_data["valid_to"])
    input(" [!] | Press to continue -> ")

if __name__ == "__pinglink__":
    pinglink()
