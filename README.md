# Braf - Web Directory & LFI Enumerator


**Braf** is a lightweight, multi-threaded command-line tool designed for efficient web directory brute-forcing and Local File Inclusion (LFI) vulnerability detection. Built with performance in mind, it utilizes thread pooling to maximize throughput while offering customizable speed controls to evade WAFs or rate limits.

-----

## 🚀 Features

  * **Dual Attack Modes:** Support for both Directory Enumeration (`dir`) and Local File Inclusion (`lfi`) discovery.
  * **Multi-Threaded:** Optimized using `ThreadPoolExecutor` for high-speed scanning.
  * **Speed Control:** 5 distinct speed levels to balance between performance and stealth.
  * **Aggressive Mode:** Optional SSL verification bypass for testing targets with self-signed or invalid certificates.
  * **Smart Detection:**
      * **Dir:** Filters responses based on standard HTTP status codes (200, 301, 403, etc.).
      * **LFI:** pattern matching for common system file signatures (e.g., `root:x:0:0`, `win.ini`).
  * **Customizable:** Support for custom wordlists and verbose logging.

-----

## 📦 Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/photomanai/Braf.git
    cd Braf
    ```

2.  **Install dependencies:**
    Braf relies on the `requests` library.

    ```bash
    pip install requests
    ```

3.  **Prepare Wordlists:**
    By default, Braf looks for a wordlist at `payloads/common.txt`. Ensure this directory exists or specify a custom path.

    ```bash
    mkdir payloads
    # Add your wordlist here, e.g., common.txt
    ```

-----

## 📖 Usage

Run the script using Python 3. Below is the help menu and argument breakdown.

```bash
python braf.py -u <TARGET_URL> [OPTIONS]
```

### Arguments

| Flag | Long Flag | Description | Default |
| :--- | :--- | :--- | :--- |
| `-u` | `--url` | **Required.** The target URL (e.g., `https://example.com`). | N/A |
| `-A` | `--attackType` | The mode of attack: `dir` or `lfi`. | `dir` |
| `-w` | `--wordlist` | Path to a custom wordlist file. | `./payloads/common.txt` |
| `-T` | `--speed` | Thread speed level (1-5). Level 5 is fastest (200 threads). | `2` |
| `-y` | N/A | Enable **Aggressive Mode** (Disables SSL/Verify check). | `False` |
| `-v` | N/A | Enable verbose output (shows 404s/failures). | `False` |

-----

## ⚡ Examples

### 1\. Basic Directory Scan

Scans for directories using the default wordlist and moderate speed.

```bash
python braf.py -u https://target.com
```

### 2\. High-Speed Aggressive Scan

Scans at maximum speed (Level 5) and ignores SSL certificate errors.

```bash
python braf.py -u https://target.com -T 5 -y
```

### 3\. LFI Vulnerability Scan

Scans a specific endpoint for LFI vulnerabilities using a custom fuzzing list.

```bash
python braf.py -u "https://target.com/vuln.php?page=" -A lfi -w ./payloads/lfi_payloads.txt
```

### 4\. Stealth/Low-Noise Scan

Scans slowly (Level 1) to avoid triggering rate limits.

```bash
python braf.py -u https://target.com -T 1
```

-----

## ⚠️ Legal Disclaimer

**Braf** is intended for educational purposes and legal penetration testing only.

  * Do not use this tool on systems you do not own or do not have explicit permission to test.
  * The author is not responsible for any misuse or damage caused by this program.
  * Usage of this tool for attacking targets without prior mutual consent is illegal.

-----

## 🤝 Contributing

Contributions are welcome\! Please feel free to submit a Pull Request.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request
