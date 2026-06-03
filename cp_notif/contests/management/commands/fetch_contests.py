from django.core.management.base import BaseCommand

from contests.scrapers.lc import fetch_leetcode_contests
from contests.scrapers.cf import fetch_codeforces_contests

from contests.services import save_contests


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        leetcode = fetch_leetcode_contests()
        codeforces = fetch_codeforces_contests()

        save_contests(leetcode)
        save_contests(codeforces)

        self.stdout.write(
            self.style.SUCCESS(
                f"Saved {len(leetcode) + len(codeforces)} contests"
            )
        )