from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail

from contests.models import Contest, ContestNotification


class Command(BaseCommand):
    help = "Send upcoming contest notifications"

    def handle(self, *args, **kwargs):
        now = timezone.now()

        for c in Contest.objects.filter(notify=True):

            time_left = c.start_time - now

            if time_left.total_seconds() <= 0:
                continue

            stage = None

            
            if time_left <= timedelta(hours=1):
                stage = "1h"
            elif time_left <= timedelta(days=3):
                stage = "2d"
            elif time_left <= timedelta(days=7):
                stage = "7d"

            if not stage:
                continue

            if ContestNotification.objects.filter(contest=c, stage=stage).exists():
                continue

            self.stdout.write(f"SENDING: {c.name} [{stage}]")

            print("ABOUT TO SEND EMAIL")

            send_mail(
                subject=f"[{stage}] {c.name}",
                message=f"""
Contest: {c.name}
Platform: {c.platform}
Starts: {c.start_time}
Link: {c.url}
""",
                from_email="ynbutterflyli@gmail.com",
                recipient_list=["ynbutterflyli@gmail.com"],
            )

            ContestNotification.objects.create(contest=c, stage=stage)