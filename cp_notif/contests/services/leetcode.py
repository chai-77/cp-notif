import requests
from datetime import datetime, timezone
import time

LEETCODE_URL = "https://leetcode.com/graphql"

QUERY = """
query {
  allContests {
    title
    titleSlug
    startTime
    duration
  }
}
"""

session = requests.Session()

def fetch_leetcode_contests(retries=3):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://leetcode.com/contest/"
    }

    payload = {"query": QUERY}

    for attempt in range(retries):
        try:
            res = session.post(
                LEETCODE_URL,
                json=payload,
                headers=headers,
                timeout=20  # increased timeout
            )

            # If server gives bad HTTP status
            res.raise_for_status()

            # Protect against empty / HTML responses
            if not res.text.strip():
                raise ValueError("Empty response from server")

            data = res.json()

            if "errors" in data:
                raise ValueError(f"GraphQL error: {data['errors']}")

            contests_data = data.get("data", {}).get("allContests", [])
            now = datetime.now(timezone.utc)

            contests = []

            for c in contests_data:
                start_ts = c.get("startTime")
                if not start_ts:
                    continue

                start_time = datetime.fromtimestamp(int(start_ts), tz=timezone.utc)

                if start_time < now:
                    continue

                contests.append({
                    "platform": "leetcode",
                    "external_id": c.get("titleSlug"),
                    "name": c.get("title"),
                    "start_time": start_time,
                    "duration_minutes": int(c.get("duration", 0)) // 60,
                    "url": f"https://leetcode.com/contest/{c.get('titleSlug')}/",
                })

            return contests

        except (requests.RequestException, ValueError) as e:
            print(f"Attempt {attempt + 1} failed: {e}")

            if attempt < retries - 1:
                time.sleep(2 * (attempt + 1))  # backoff
            else:
                return []

    return []


if __name__ == "__main__":
    contests = fetch_leetcode_contests()
    for c in contests:
        print(c)