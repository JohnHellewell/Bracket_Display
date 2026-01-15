import pychrome
import subprocess
import time
import os
import socket

# ---------- CONFIG ----------
URL_FILE = "links.txt"       # file in same folder as script
DISPLAY_TIME = 10
DEBUG_PORT = 9222
BROWSER = "chromium-browser"
# ----------------------------

def is_port_open(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(("127.0.0.1", port))
        s.close()
        return True
    except:
        return False

def launch_chromium(first_url):
    """Launch Chromium with first URL in initial tab."""
    print(f"Launching Chromium with {first_url}...")
    subprocess.Popen([
        BROWSER,
        "--start-fullscreen",
        "--disable-infobars",
        f"--remote-debugging-port={DEBUG_PORT}",
        first_url  # open the first URL immediately
    ])
    time.sleep(5)  # wait for Chromium to start

def read_urls():
    if not os.path.exists(URL_FILE):
        print(f"{URL_FILE} not found")
        return []
    with open(URL_FILE, "r") as f:
        return [line.strip() for line in f if line.strip()]

def open_remaining_tabs(browser, urls):
    """Open remaining URLs as new tabs after first one."""
    tabs = []
    for url in urls[1:]:
        tab = browser.new_tab()
        tab.start()
        tab.Page.navigate(url=url)
        tab.wait(2)
        tabs.append(tab)
    return tabs

def cycle_tabs(tabs):
    """Bring each tab to front in an endless loop."""
    while True:
        for tab in tabs:
            tab.Page.bring_to_front()
            time.sleep(DISPLAY_TIME)

# ---------------- MAIN ----------------
urls = read_urls()
if not urls:
    print("No URLs to display!")
    exit()

# Launch Chromium with first URL
if not is_port_open(DEBUG_PORT):
    launch_chromium(urls[0])

browser = pychrome.Browser(url=f"http://127.0.0.1:{DEBUG_PORT}")

# Give first tab a moment to attach
time.sleep(2)
all_tabs = browser.list_tab()

# Open remaining URLs
all_tabs += open_remaining_tabs(browser, urls)

# Cycle tabs endlessly
cycle_tabs(all_tabs)
