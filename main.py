import subprocess
import time

URL_FILE = "links.txt"
DISPLAY_TIME = 10  # seconds

def read_urls(filename):
    with open(filename, "r") as f:
        return [line.strip() for line in f if line.strip()]

def show_url(url):
    subprocess.run([
        "chromium-browser",
        "--start-fullscreen",
        "--noerrdialogs",
        "--disable-infobars",
        "--app=" + url
    ])

def main():
    urls = read_urls(URL_FILE)

    if not urls:
        print("No URLs found.")
        return

    while True:
        for url in urls:
            show_url(url)
            time.sleep(DISPLAY_TIME)

if __name__ == "__main__":
    main()
