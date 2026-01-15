import subprocess
import time
import os

# Path to your URLs file
URL_FILE = "links.txt"

# How long each page is displayed (seconds)
DISPLAY_TIME = 10

# Path to Chromium (or use "google-chrome")
BROWSER = "chromium-browser"

# Optional: use a dedicated profile so uBlock is loaded
USER_DATA_DIR = "/home/john/.config/signage-chrome"

def read_urls():
    """Read URLs from the text file, one per line."""
    if not os.path.exists(URL_FILE):
        print(f"{URL_FILE} not found")
        return []
    with open(URL_FILE, "r") as f:
        return [line.strip() for line in f if line.strip()]

def open_browser(url):
    """Open Chromium fullscreen with the given URL."""
    return subprocess.Popen([
        BROWSER,
        "--start-fullscreen",
        "--disable-infobars",
        f"--user-data-dir={USER_DATA_DIR}",
        url
    ])

def main():
    urls = read_urls()
    if not urls:
        print("No URLs found in file")
        return

    while True:
        for url in urls:
            print(f"Opening {url}")
            proc = open_browser(url)
            time.sleep(DISPLAY_TIME)
            proc.terminate()  # Close Chromium to go to next page
            time.sleep(1)  # Short pause to avoid overlap

if __name__ == "__main__":
    main()
