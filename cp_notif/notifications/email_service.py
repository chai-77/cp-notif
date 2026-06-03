from django.core.mail import send_mail
from django.conf import settings


def send_notification_email(user, contest):

    send_mail(
        subject=f"{contest.name} starts soon",
        message=(
            f"{contest.name} starts in "
            f"{user.reminder_minutes} minutes.\n\n"
            f"{contest.url}"
        ),
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False,
    )