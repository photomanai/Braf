import requests
import sys
import os
import argparse
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def GetUserInput():
    defaultWordListPath = os.path.join(os.getcwd(), "payloads/common.txt")
    parser = argparse.ArgumentParser(
        description="bref.py - Optimized Directory & LFI Brute Force Tool"
    )

    parser.add_argument("-u", "--url", type=str, required=True, help="Target URL")
    parser.add_argument("-y", action="store_true", help="Enable aggressive mode (verify=False)")
    parser.add_argument("-v", action="store_true", help="Enable verbose output")
    parser.add_argument(
        "-w", "--wordlist",
        metavar="PATH",
        default=defaultWordListPath,
        help=f"Wordlist path (default: {defaultWordListPath})",
    )
    parser.add_argument(
        "-T", "--speed",
        type=int,
        choices=range(1, 6),
        default=2,
        metavar="LEVEL",
        help="Speed level: 1-5 (default: 2)",
    )
    parser.add_argument("-A", "--attackType", type=str, default="dir", choices=["dir", "lfi"], help="Attack Type: dir, lfi (default: dir)")
    
    args = parser.parse_args()

    return {
        "url": args.url,
        "aggressiveMode": args.y,
        "wordListPath": args.wordlist,
        "speed": args.speed,
        "type": args.attackType.lower(),
        "verbose": args.v
    }

class Force:
    def __init__(self, userArgs):
        self.userArgs = userArgs
        self.url = self.normalize_url(userArgs["url"])
        self.word_list_path = userArgs["wordListPath"]
        self.status_codes = {200, 201, 204, 301, 302, 307, 401, 403}
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (BrefTool/Optimized)'
        })
        
        self.max_workers = self.calculate_workers(userArgs["speed"])

    def calculate_workers(self, level):
        mapping = {1: 10, 2: 25, 3: 50, 4: 100, 5: 200}
        return mapping.get(level, 25)

    def normalize_url(self, url):
        parsed = urlparse(url)
        if not parsed.scheme:
            return f"https://{url}"
        return url

    def check(self, payload):
        target_url = ""
        try:
            if self.userArgs["type"] == "dir":
                target_url = urljoin(self.url, payload)
            else: 
                target_url = self.url + payload

            verify_ssl = not self.userArgs["aggressiveMode"]
            r = self.session.get(target_url, timeout=5, allow_redirects=True, verify=verify_ssl)

            if self.userArgs["type"] == "dir":
                if r.status_code in self.status_codes:
                    print(f"[+] {r.status_code} | Size: {len(r.text):>6} | URL: {target_url}")
                elif self.userArgs["verbose"]:
                    print(f"[-] {r.status_code} -> {target_url}")

            elif self.userArgs["type"] == "lfi":
                if "root:x:0:0" in r.text or "win.ini" in r.text:
                    print(f"[!!!] LFI VULN FOUND: {payload}")
                    print(f"      Size: {len(r.text)} | Status: {r.status_code}")
                elif self.userArgs["verbose"]:
                    print(f"[-] {r.status_code} -> {payload}")

        except requests.RequestException:
            pass
        except Exception as e:
            print(f"[!] Error processing {payload}: {e}")

    def get_payload_generator(self):
        if not os.path.exists(self.word_list_path):
            print(f"[!] Wordlist not found: {self.word_list_path}")
            sys.exit(1)

        with open(self.word_list_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                stripped = line.strip()
                if stripped:
                    yield stripped

    def run(self):
        print(f"[+] Target: {self.url}")
        print(f"[+] Workers: {self.max_workers}")
        print(f"[+] Attack Type: {self.userArgs['type'].upper()}")
        print("[+] Starting brute force...\n")

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            try:
                executor.map(self.check, self.get_payload_generator())
            except KeyboardInterrupt:
                print("\n[!] Stopping workers...")
                executor.shutdown(wait=False)
                raise

def main():
    try:
        userArgs = GetUserInput()
        force = Force(userArgs)
        force.run()
    except KeyboardInterrupt:
        print("\n[!] User aborted. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"[!] Critical Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()