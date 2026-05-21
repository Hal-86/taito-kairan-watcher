import requests
from bs4 import BeautifulSoup
import hashlib
import os

URL = "https://www.city.taito.lg.jp/kurashi/kyodo/tyoukai/kairan.html"

WEBHOOK_URL = os.environ["DISCORD_WEBHOOK"]

response = requests.get(URL)

soup = BeautifulSoup(response.text, "html.parser")

main_text = soup.get_text()

current_hash = hashlib.sha256(main_text.encode()).hexdigest()

HASH_FILE = "last_hash.txt"

old_hash = ""

if os.path.exists(HASH_FILE):
    with open(HASH_FILE, "r") as f:
        old_hash = f.read()

if current_hash != old_hash:

    requests.post(
        WEBHOOK_URL,
        json={
            "content":
            f"【台東区回覧 更新】\n{URL}"
        }
    )

    with open(HASH_FILE, "w") as f:
        f.write(current_hash)

    print("更新あり！")
else:
    print("更新なし")
