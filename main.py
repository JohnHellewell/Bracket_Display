import subprocess
import time
import os

# ---------- CONFIG ----------
URL_FILE = "links.txt"       # file in same folder as script
DISPLAY_TIME = 10            # seconds per window
BROWSER = "chromium-browser"
# ----------------------------

def read_urls():
    """Read URLs from the text file, one per line."""
    if not os.path.exists(URL_FILE):
        print(f"{URL_FILE} not found")
        return []
    with open(URL_FILE, "r") as f:
        return [line.strip() for line in f if line.strip()]

def open_windows(urls):
    """Open each URL in a separate Chromium window."""
    procs = []
    for url in urls:
        print(f"Opening {url}")
        proc = subprocess.Popen([
            BROWSER,
            "--start-fullscreen",
            "--disable-infobars",
            "--new-window",
            "--no-sandbox",      # avoid Snap/AppArmor issues
            url
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)  # suppress warnings
        procs.append(proc)
        time.sleep(2)  # small delay to let window open
    return procs

def get_window_ids():
    """Return list of Chromium window IDs using wmctrl."""
    output = subprocess.check_output(["wmctrl", "-l"]).decode()
    window_ids = []
    for line in output.splitlines():
        if "Chromium" in line:
            window_ids.append(line.split()[0])
    return window_ids

def cycle_windows(window_ids):
    """Bring each window to front in an endless loop."""
    while True:
        for wid in window_ids:
            subprocess.run(["wmctrl", "-i", "-a", wid])
            time.sleep(DISPLAY_TIME)

# ---------------- MAIN ----------------
urls = read_urls()
if not urls:
    print("No URLs to display!")
    exit()

# Open one window per URL
open_windows(urls)
time.sleep(3)  # let windows attach

# Get window IDs and cycle through them
window_ids = get_window_ids()
if not window_ids:
    print("No Chromium windows detected!")
    exit()

cycle_windows(window_ids)
