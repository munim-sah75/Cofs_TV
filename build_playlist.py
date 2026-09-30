import json, urllib.parse

BASE = "http://198.195.239.50/"   # for turning relative logo paths into full URLs
INCLUDE_HIDDEN = False

with open("tv_channels.json", "r", encoding="utf-8") as f:
    data = json.load(f)

lines = ["#EXTM3U"]
count = 0

for c in data.get("channels", []):
    url = c.get("url")
    if not url:
        continue
    if not INCLUDE_HIDDEN and c.get("status", "visible") != "visible":
        continue

    name = c.get("name", "Unknown").replace(",", " ").strip()
    group = c.get("category", "Other")
    logo = c.get("logo", "")
    logo_url = BASE + urllib.parse.quote(logo) if logo and not logo.startswith("http") else logo

    lines.append(f'#EXTINF:-1 tvg-name="{name}" tvg-logo="{logo_url}" group-title="{group}",{name}')
    lines.append(url)
    count += 1

if count == 0:
    raise SystemExit("No channels found - check the JSON file.")

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

print(f"Wrote {count} channels")
