# BruteForce Tool for dir Search/LFI

import requests
import sys
import os
import argparse
from urllib.parse import urljoin, urlparse

def GetUserInput():
    defaultWordListPath = os.path.join(os.getcwd(), "payloads/common.txt")
    parser = argparse.ArgumentParser(
        description="bref.py - Works with url and optional parameters"
    )

    parser.add_argument("-u", "--url", type=str,required=True, help="url to brute")

    # parser.add_argument("-t", "--test", type=str, help="Test message", default=None)

    parser.add_argument("-y", action="store_true", help="Enable aggressive mode")
    parser.add_argument(
        "-w",
        "--wordlist",
        metavar="PATH",
        default=defaultWordListPath,
        help=f"word list directory (default: {defaultWordListPath}",
    )
    parser.add_argument(
        "-T",
        "--speed",
        type=int,
        choices=range(1, 6),
        default=2,
        metavar="LEVEL",
        help="Speed level: 0‑5 (default: %(default)s)",
    )
    args = parser.parse_args()

    return {
        "url": args.url,
        "aggressiveMode": args.y,
        "wordListPath": args.wordlist,
        "speed": args.speed,
    }
        # "testMessage": args.test,



class Force:
    def __init__(self, url, word_list_path):
        self.url = url
        self.word_list_path = word_list_path
        self.status_code = [200, 201, 204, 301, 302, 307, 401, 403]
        self.normalize_url()

    def normalize_url(self):
        parsed = urlparse(self.url)
        if not parsed.scheme:
            self.url = f"https://{self.url}"

    def lfi_brute(self):
        with open(self.word_list_path, "r") as f:
            payloads = [line.strip() for line in f if line.strip()]

        print(f"[+] Payload lines: {len(payloads)}")

        for payload in payloads:
            try:
                r = requests.get(self.url + payload, timeout=5)
                if "root:" in r.text or len(r.text) > 320:
                    print(f"[+] VULN!: {payload}")
                    print(f"    length: {len(r.text)} | Status: {r.status_code}")
                else:
                    print(f"[-] Code: {r.status_code}")
            except Exception as e:
                print(f"[!]ERROR: {e}")

    def dir_brute(self):
        with open(self.word_list_path, "r") as f:
            payloads = [line.strip() for line in f if line.strip()]

        print(f"[+] Payload lines: {len(payloads)}")

        # os.path.join(os.getcwd(), "payloads/common.txt")
        for payload in payloads:
            try:
                # fu = f"{self.url}/{payload}"
                fu = urljoin(self.url, payload)
                print(fu)
                r = requests.get(fu, timeout=5)
                if self.status_code in r.status_code or len(r.text) > 320:
                    print(f"[+] VULN!: {payload}")
                    print(f"    length: {len(r.text)} | Status: {r.status_code}")
                else:
                    print(f"[-] Code: {r.status_code}")
            except Exception as e:
                print(f"[!]ERROR: {e}")


def main():
    try:
        userArgs = GetUserInput()
        force = Force(userArgs["url"], userArgs["wordListPath"])
        force.dir_brute()
    except KeyboardInterrupt:
        print("EXIT...")
        sys.exit(1)
    except Exception as e:
        print(f"[!] ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()