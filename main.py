import subprocess
import os
import time

# ---------- CONFIG ----------
URL_FILE = "links.txt"           # file with one URL per line
BROWSER_CMD = "google-chrome"    # default Chrome command
STARTUP_DELAY = 5                # seconds to wait for Chrome to start before opening tabs
TAB_DELAY = 1                    # seconds between opening each tab
# ----------------------------

def read_urls():
    """Read URLs from the text file."""
    if not os.path.exists(URL_FILE):
        print(f"{URL_FILE} not found!")
        return []
    with open(URL_FILE, "r") as f:
        return [line.strip() for line in f if line.strip()]

def open_tabs(urls):
    """Open each URL in Chrome tabs, first one fullscreen."""
    if not urls:
        return

    # Open first tab with fullscreen
    first_url = urls[0]
    print(f"Opening first tab: {first_url}")
    subprocess.Popen([
        BROWSER_CMD,
        "--start-fullscreen",
        "--disable-infobars",
        "--password-store=basic",
        first_url
    ])

    # Give Chrome time to fully start
    time.sleep(STARTUP_DELAY)

    # Open remaining tabs
    for url in urls[1:]:
        print(f"Opening tab: {url}")
        subprocess.Popen([
            BROWSER_CMD,
            "--new-tab",
            "--disable-infobars",
            "--password-store=basic",
            url
        ])
        time.sleep(TAB_DELAY)

if __name__ == "__main__":
    urls = read_urls()
    if not urls:
        print("No URLs to open. Exiting.")
    else:
        open_tabs(urls)
        print("All tabs opened. Tab Revolver – Auto Rotate Tabs will handle cycling automatically.")
