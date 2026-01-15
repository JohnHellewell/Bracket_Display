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

# Check if remote debugging port is open
def is_port_open(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(("127.0.0.1", port))
        s.close()
        return True
    except:
        return False

# Launch Chromium with remote debugging if not running
def launch_chromium():
    print("Launching Chromium...")
    subprocess.Popen([
        BROWSER,
        "--start-fullscreen",
        "--disable-infobars",
        f"--remote-debugging-port={DEBUG_PORT}"
    ])
    time.sleep(5)  # give it a moment to start

# Read URLs from file
def read_urls():
    if not os.path.exists(URL_FILE):
        print(f"{URL_FILE} not found")
        return []
    with open(URL_FILE, "r") as f:
        return [line.strip() for line in f if line.strip()]

# Open URLs in separate tabs
def open_tabs(browser, urls):
    tabs = []
    if not urls:
        return tabs

    # First URL in first tab
    tabs.append(browser.new_tab())
    tabs[0].start()
    tabs[0].Page.navigate(url=urls[0])
    tabs[0].wait(2)

    # Remaining URLs in new tabs
    for url in urls[1:]:
        tab = browser.new_tab()
        tab.start()
        tab.Page.navigate(url=url)
        tab.wait(2)
        tabs.append(tab)

    return tabs

# Cycle through tabs smoothly
def cycle_tabs(tabs):
    while True:
        for tab in tabs:
            tab.Page.bring_to_front()  # focus this tab
            time.sleep(DISPLAY_TIME)

# ---------------------------- MAIN ----------------------------
if not is_port_open(DEBUG_PORT):
    launch_chromium()

browser = pychrome.Browser(url=f"http://127.0.0.1:{DEBUG_PORT}")

urls = read_urls()
if not urls:
    print("No URLs to display!")
    exit()

tabs = open_tabs(browser, urls)
cycle_tabs(tabs)
