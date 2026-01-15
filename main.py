import pychrome
import time

URL_FILE = "links.txt"
DISPLAY_TIME = 10
DEBUG_PORT = 9222

def read_urls():
    with open(URL_FILE) as f:
        return [line.strip() for line in f if line.strip()]

urls = read_urls()

browser = pychrome.Browser(url=f"http://127.0.0.1:{DEBUG_PORT}")
tabs = browser.list_tab()
tab = tabs[0] if tabs else browser.new_tab()
tab.start()

while True:
    for url in urls:
        tab.Page.navigate(url=url)
        tab.wait(2)  # wait for page to load
        time.sleep(DISPLAY_TIME)
