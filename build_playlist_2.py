import json, urllib.parse

BASE = "http://103.151.60.188:12345"   # for relative logo paths like /tvlogo/TSports.jpg
SKIP_PRIVATE_IPS = True                # skip 192.168.x.x, 10.x.x.x, 172.16-31.x.x, 127.x
REPLACE_DOTS = True                    # "Star.Sports.1.HD" -> "Star Sports 1 HD"

def is_private(url):
    host = urllib.parse.urlparse(url).hostname or ""
    return host.startswith(("192.168.", "10.", "127.")) or \
           any(host.startswith(f"172.{i}.") for i in range(16, 32))

with open("channels.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Accept both a plain list and {"channels": [...]}
channels = data if isinstance(data, list) else data.get("channels", [])

lines = ["#EXTM3U"]
count = skipped = 0

for c in channels:
    url = c.get("url")
    if not url:
        continue
    if SKIP_PRIVATE_IPS and is_private(url):
        skipped += 1
        continue

    name = c.get("name", "Unknown").replace(",", " ")
    if REPLACE_DOTS:
        name = name.replace(".", " ")
    name = " ".join(name.split())

    group = c.get("category", "Other")
    tvg_id = c.get("id", "")
    logo = c.get("logo", "")
    if logo and not logo.startswith("http"):
        logo = BASE + "/" + logo.lstrip("/")

    lines.append(f'#EXTINF:-1 tvg-id="{tvg_id}" tvg-name="{name}" tvg-logo="{logo}" group-title="{group}",{name}')
    lines.append(url)
    count += 1

if count == 0:
    raise SystemExit("No channels found - check the JSON file.")

with open("playlist_2.m3u", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

print(f"Wrote {count} channels, skipped {skipped} private-IP channels")
