from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from contests.models import Contest, ReminderRule
from notifications.models import Notification
from django.contrib.auth import get_user_model
from django.core.mail import send_mail


User = get_user_model()

class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        now = timezone.now()

        rules = ReminderRule.objects.select_related("contest").all()

        for rule in rules:

            contest = rule.contest

            send_time = contest.start_time - timedelta(minutes=rule.offset_minutes)

            # if it's time to send
            if now >= send_time:

                if Notification.objects.filter(
                    contest=contest,
                    stage=rule.label
                ).exists():
                    continue

                # send email
                for user in User.objects.all():
                    if not user.email:
                        continue

                send_mail(
                    subject=f"{contest.name} reminder ({rule.label})",
                    message=f"""
                Hi {user.username},

                Contest: {contest.name}
                Starts at: {contest.start_time}
                Reminder: {rule.label}
                """,
                    from_email="noreply@cpnotif.com",  # or None if configured in settings
                    recipient_list=[user.email],
                )

                Notification.objects.create(
                    contest=contest,
                    stage=rule.label
                )