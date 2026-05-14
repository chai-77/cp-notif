import requests
from datetime import datetime, timezone

CF_API = "https://codeforces.com/api/contest.list"

def fetch_codeforces_contests():
    res = requests.get(CF_API)
    data = res.json()

    if data["status"] != "OK":
        raise Exception("Codeforces API error")

    contests = []

    for c in data["result"]:
        # We only want upcoming contests
        if c["phase"] != "BEFORE":
            continue

        start_time = datetime.fromtimestamp(c["startTimeSeconds"], tz=timezone.utc)

        contests.append({
            "platform": "codeforces",
            "external_id": str(c["id"]),
            "name": c["name"],
            "start_time": start_time,
            "duration_minutes": c["durationSeconds"] // 60,
            "url": f"https://codeforces.com/contests/{c['id']}",
            "difficulty": None
        })

    return contests


if __name__ == "__main__":
    contests = fetch_codeforces_contests()
    for c in contests:
        print(c)
