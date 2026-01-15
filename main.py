import subprocess, time

urls = ["https://example.com", "https://openai.com"]
while True:
    for url in urls:
        proc = subprocess.Popen([
            "chromium-browser",
            "--start-fullscreen",
            "--disable-infobars",
            url
        ])
        time.sleep(10)
        proc.terminate()
        time.sleep(1)
