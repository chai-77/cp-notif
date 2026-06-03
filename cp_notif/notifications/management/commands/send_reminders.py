from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from contests.models import Contest
from notifications.models import Notification
from django.contrib.auth import get_user_model
from django.core.mail import send_mail


User = get_user_model()

class Command(BaseCommand):
    help = "Send contest reminders"

    def handle(self, *args, **kwargs):

        now = timezone.now()
        users = User.objects.all()
        contests = Contest.objects.all()

        sent_count = 0

        for contest in contests:

            time_left = contest.start_time - now

            if time_left <= timedelta(0):
                continue

            # 1 HOUR FIRST (more specific)
            if time_left <= timedelta(hours=1):

                if not Notification.objects.filter(
                    contest=contest,
                    stage="1h"
                ).exists():

                    for user in users:
                        if not user.email:
                            continue

                        send_mail(
                            subject=f"{contest.name} starts in 1 hour!",
                            message=f"""
Hi {user.username},

Contest: {contest.name}
Starts: {contest.start_time}
Time left: 1 hour

Link: {contest.url}
""",
                            from_email=None,
                            recipient_list=[user.email],
                        )

                    Notification.objects.create(
                        contest=contest,
                        stage="1h"
                    )

                    sent_count += 1

            # 4 DAYS AFTER
            elif time_left <= timedelta(days=4):

                if not Notification.objects.filter(
                    contest=contest,
                    stage="4d"
                ).exists():

                    for user in users:
                        if not user.email:
                            continue

                        send_mail(
                            subject=f"{contest.name} starts soon ",
                            message=f"""
Hi {user.username},

Contest: {contest.name}
Starts: {contest.start_time}
Time left: < 4 days

Link: {contest.url}
""",
                            from_email=None,
                            recipient_list=[user.email],
                        )

                    Notification.objects.create(
                        contest=contest,
                        stage="4d"
                    )

                    sent_count += 1

        self.stdout.write(
            self.style.SUCCESS(f"Sent {sent_count} reminders")
        )