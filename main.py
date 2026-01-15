import subprocess
import time
import os

URL_FILE = "links.txt"
DISPLAY_TIME = 10
BROWSER = "chromium-browser"
USER_DATA_DIR = "/home/john/.config/signage-chrome"

def read_urls():
    """Read URLs from the text file, one per line."""
    if not os.path.exists(URL_FILE):
        print(f"{URL_FILE} not found")
        return []
    with open(URL_FILE, "r") as f:
        return [line.strip() for line in f if line.strip()]

def open_tabs(urls):
    """Open all URLs in separate tabs in one Chromium window."""
    if not urls:
        return None

    # Open the first URL to start a window
    proc = subprocess.Popen([
        BROWSER,
        "--start-fullscreen",
        "--disable-infobars",
        f"--user-data-dir={USER_DATA_DIR}",
        urls[0]
    ])
    time.sleep(3)  # wait for window to open

    # Open remaining URLs in new tabs
    for url in urls[1:]:
        subprocess.Popen([
            BROWSER,
            "--new-tab",
            f"--user-data-dir={USER_DATA_DIR}",
            url
        ])
        time.sleep(1)  # small delay to let tabs load

    return proc

def cycle_tabs(url_count):
    """Cycle through tabs using Ctrl+Tab."""
    import subprocess
    while True:
        for _ in range(url_count):
            # Ctrl+Tab switches to next tab
            subprocess.run(["xdotool", "key", "ctrl+Tab"])
            time.sleep(DISPLAY_TIME)

def main():
    urls = read_urls()
    if not urls:
        print("No URLs to open")
        return

    proc = open_tabs(urls)
    if not proc:
        return

    # Give all tabs a moment to load
    time.sleep(5)
    cycle_tabs(len(urls))

if __name__ == "__main__":
    main()
