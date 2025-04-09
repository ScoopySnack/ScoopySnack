import requests
from collections import Counter
from datetime import datetime
import re

username = "ScoopySnack"

events = []
page = 1
while page <= 5:
    r = requests.get(f"https://api.github.com/users/{username}/events/public?page={page}")
    data = r.json()
    if not data or "message" in data:
        break
    for event in data:
        if 'created_at' in event:
            day = datetime.strptime(event['created_at'], "%Y-%m-%dT%H:%M:%SZ").strftime('%A')
            events.append(day)
    page += 1

if events:
    count = Counter(events)
    most_active_day = count.most_common(1)[0][0]
else:
    most_active_day = "No public activity yet."

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

start_tag = "<!-- ACTIVITY-DAY-START -->"
end_tag = "<!-- ACTIVITY-DAY-END -->"
new_line = f"{start_tag}\n**Most Active Day:** _{most_active_day}_ 🌟\n{end_tag}"

updated_readme = re.sub(
    f"{start_tag}.*?{end_tag}",
    new_line,
    readme,
    flags=re.DOTALL
)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(updated_readme)
