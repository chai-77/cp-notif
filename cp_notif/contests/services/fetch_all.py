from .codeforces import fetch_codeforces_contests
from .leetcode import fetch_leetcode_contests
from .sync import sync_contests


def run_sync():
    contests = []

    contests += fetch_codeforces_contests()
    contests += fetch_leetcode_contests()

    sync_contests(contests)
    print(f"Synced {len(contests)} contests")