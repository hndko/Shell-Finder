#!/usr/bin/env python3
import sys
import argparse
import time
import urllib.request
import urllib.error
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

# ANSI Colors
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
]

def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Colors.CYAN + """
|------------------------------------------------------------------------------|
|                        Shell Finder PRO (Python 3)                           |
|------------------------------------------------------------------------------|
|                                                                              |
|                 Updates by:         [  YourName/Refactor  ]                  |
|                 Original by:        [  exploit1337        ]                  |
|                                                                              |
|------------------------------------------------------------------------------|
""" + Colors.RESET)

def get_arguments():
    parser = argparse.ArgumentParser(description=f"{Colors.BOLD}Advanced Shell Finder{Colors.RESET}")
    parser.add_argument("-u", "--url", dest="url", help="Target URL (e.g., http://example.com)", required=False)
    parser.add_argument("-w", "--wordlist", dest="wordlist", help="Path to dictionary file", default="dictionary")
    parser.add_argument("-t", "--threads", dest="threads", help="Number of threads", type=int, default=10)

    options = parser.parse_args()
    if not options.url:
        # Fallback to interactive mode if no arguments provided
        print_banner()
        options.url = input(f"{Colors.YELLOW}\nEnter URL to scan [eg, http://sitename.com]: {Colors.RESET}")

    return options

def check_url(target_url, path, timeout=5):
    full_url = f"{target_url}/{path}" if not target_url.endswith('/') else f"{target_url}{path}"
    try:
        req = urllib.request.Request(
            full_url,
            headers={'User-Agent': random.choice(USER_AGENTS)}
        )
        with urllib.request.urlopen(req, timeout=timeout) as response:
            if response.getcode() == 200:
                return (True, full_url)
    except urllib.error.HTTPError as e:
        if e.code == 200: # Sometimes HTTPError can still return 200? unlikely but safe
             return (True, full_url)
    except urllib.error.URLError:
        pass
    except Exception:
        pass
    return (False, full_url)

def main():
    options = get_arguments()
    target_url = options.url
    if not target_url.startswith("http"):
        target_url = "http://" + target_url

    print(f"\n{Colors.BLUE}[*] Target: {target_url}{Colors.RESET}")
    print(f"{Colors.BLUE}[*] Threads: {options.threads}{Colors.RESET}")
    print(f"{Colors.BLUE}[*] Wordlist: {options.wordlist}{Colors.RESET}")

    try:
        with open(options.wordlist, "r") as f:
            paths = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"{Colors.RED}[!] Dictionary file '{options.wordlist}' not found.{Colors.RESET}")
        sys.exit(1)

    print(f"{Colors.BLUE}[*] Loaded {len(paths)} payloads. Starting scan...{Colors.RESET}\n")

    found_shells = []
    start_time = time.time()

    try:
        with ThreadPoolExecutor(max_workers=options.threads) as executor:
            futures = {executor.submit(check_url, target_url, path): path for path in paths}

            for future in as_completed(futures):
                is_found, url = future.result()
                if is_found:
                    print(f"{Colors.GREEN}[+] FOUND: {url}{Colors.RESET}")
                    found_shells.append(url)
                    # Optional: Write to log immediately
                else:
                    # Overwrite line to show progress
                    sys.stdout.write(f"\r{Colors.YELLOW}[~] Scanning... {url[:50].ljust(50)}{Colors.RESET}")
                    sys.stdout.flush()

    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[!] Scan interrupted by user.{Colors.RESET}")
        sys.exit(0)

    print(f"\n\n{Colors.CYAN}|------------------------------------------------------------------------------|{Colors.RESET}")
    print(f"{Colors.CYAN}|                            Scan Completed                                    |{Colors.RESET}")
    print(f"{Colors.CYAN}|------------------------------------------------------------------------------|{Colors.RESET}")
    print(f"Time Taken: {time.time() - start_time:.2f} seconds")
    print(f"Total Found: {len(found_shells)}")

    if found_shells:
        print(f"\n{Colors.GREEN}Possible Shells:{Colors.RESET}")
        for shell in found_shells:
            print(f" - {shell}")

        # Save to log
        log_name = f"scan_{int(time.time())}.log"
        with open(log_name, "w") as f:
            f.write("\n".join(found_shells))
        print(f"\n{Colors.BLUE}[*] Saved results to {log_name}{Colors.RESET}")
    else:
        print(f"\n{Colors.RED}No shells found.{Colors.RESET}")

if __name__ == "__main__":
    main()
