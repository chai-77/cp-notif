from .models import Contest, ReminderRule

def save_contests(contests_data):

    for data in contests_data:

        contest, created = Contest.objects.update_or_create(
            platform=data["platform"],
            contest_id=data["contest_id"],
            defaults={
                "name": data["name"],
                "start_time": data["start_time"],
                "duration_minutes": data["duration_minutes"],
                "url": data["url"],
            }
        )

        # create rules when contest is new
        if created:

            ReminderRule.objects.create(
                contest=contest,
                offset_minutes=5760,  # 4 days
                label="4d"
            )

            ReminderRule.objects.create(
                contest=contest,
                offset_minutes=60,  # 1 hour
                label="1h"
            )