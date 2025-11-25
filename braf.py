# BruteForce Tool for dir Search/LFI

import requests
import sys
import os
import argparse
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor

def GetUserInput():
    defaultWordListPath = os.path.join(os.getcwd(), "payloads/common.txt")
    parser = argparse.ArgumentParser(
        description="bref.py - Works with url and optional parameters"
    )

    parser.add_argument("-u", "--url", type=str,required=True, help="url to brute")

    # parser.add_argument("-t", "--test", type=str, help="Test message", default=None)

    parser.add_argument("-y", action="store_true", help="Enable aggressive mode")
    parser.add_argument("-v", action="store_true", help="Enable verbose")
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
    parser.add_argument("-A", "--attackType", type=str, default="dir", help="Choose Your Attack Type: dir, lfi (default: dir)")
    args = parser.parse_args()

    return {
        "url": args.url,
        "aggressiveMode": args.y,
        "wordListPath": args.wordlist,
        "speed": args.speed,
        "type": args.attackType,
        "verbose": args.v
    }
        # "testMessage": args.test,



class Force:
    def __init__(self, url, word_list_path, userArgs):
        self.url = url
        self.word_list_path = word_list_path
        self.status_codes = [200, 201, 204, 301, 302, 307, 401, 403]
        self.userArgs = userArgs
        self.normalize_url()

    def normalize_url(self):
        parsed = urlparse(self.url)
        if not parsed.scheme:
            self.url = f"https://{self.url}"

    def check(self, url,payload):
        fu = urljoin(self.url, payload)
        try:
            r = requests.get(fu, timeout=7, allow_redirects=True)
            if self.userArgs["type"].lower() == "dir":
                if r.status_code in self.status_codes:
                    print(f"[+] {r.status_code} {len(r.text):>6} → {fu}")
                    #    print(f"{'payload:':>25} {payload}")
                elif self.userArgs["verbose"]:
                    print(f"[-] Code: {r.status_code}")
            elif self.userArgs["type"].lower() == "lfi":
                if "root:" in r.text: # or len(r.text) > 320
                    print(f"[+] VULN!: {payload}")
                    print(f"    length: {len(r.text)} | Status: {r.status_code}")
                elif self.userArgs["verbose"]:
                    print(f"[-] Code: {r.status_code}")
        except Exception as e:
            print(f"[!]ERROR: {e}")


    def lfi_brute(self):
        print("[+] Entered LFi type attack")
        with open(self.word_list_path, "r") as f:
            payloads = [line.strip() for line in f if line.strip()]

        print(f"[+] Payload lines: {len(payloads)}")


        with ThreadPoolExecutor(max_workers=100) as executor:
            executor.map(lambda p: self.check(self.url, p), payloads)

        # for payload in payloads:
        #     try:
        #         r = requests.get(self.url + payload, timeout=5)
        #         if "root:" in r.text: # or len(r.text) > 320
        #             print(f"[+] VULN!: {payload}")
        #             print(f"    length: {len(r.text)} | Status: {r.status_code}")
        #         else:
        #             print(f"[-] Code: {r.status_code}")
        #     except Exception as e:
        #         print(f"[!]ERROR: {e}")

    def dir_brute(self):
        print("[+] Entered DIR type attack")
        with open(self.word_list_path, "r") as f:
            payloads = [line.strip() for line in f if line.strip()]

        print(f"[+] Payload lines: {len(payloads)}")

        with ThreadPoolExecutor(max_workers=100) as executor:
            executor.map(lambda p: self.check(self.url, p), payloads)


def main():
    try:
        userArgs = GetUserInput()
        force = Force(userArgs["url"], userArgs["wordListPath"], userArgs)
        if userArgs["type"].lower() == "dir":
            force.dir_brute()
        elif userArgs["type"].lower() == "lfi":
            force.lfi_brute()
        else:
            print(f"[!] ERROR: {userArgs["type"]} attack type not exist")
    except KeyboardInterrupt:
        print("EXIT...")
        sys.exit(1)
    except Exception as e:
        print(f"[!] ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()