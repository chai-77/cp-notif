import requests
from datetime import datetime, timezone

CF_API = "https://codeforces.com/api/contest.list"

def fetch_codeforces_contests():
    try:
        res = requests.get(CF_API, timeout=20)
        res.raise_for_status()
        data = res.json()

    except requests.RequestException as e:
        print(f"Network error: {e}")
        return []

    except ValueError as e:
        print(f"Invalid JSON response: {e}")
        return []

    if data.get("status") != "OK":
        print("Codeforces API error:", data)
        return []

    contests = []

    for c in data.get("result", []):
        try:
            if c.get("phase") != "BEFORE":
                continue

            start_ts = c.get("startTimeSeconds")
            if not start_ts:
                continue

            start_time = datetime.fromtimestamp(start_ts, tz=timezone.utc)

            contests.append({
                "platform": "codeforces",
                "external_id": str(c.get("id")),
                "name": c.get("name"),
                "start_time": start_time,
                "duration_minutes": c.get("durationSeconds", 0) // 60,
                "url": f"https://codeforces.com/contests/{c.get('id')}",
                "contest_type": c.get("type")
            })

        except Exception as e:
            print(f"Skipping contest due to error: {e}")
            continue

    return contests


if __name__ == "__main__":
    contests = fetch_codeforces_contests()
    for c in contests:
        print(c)