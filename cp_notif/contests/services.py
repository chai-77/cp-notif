from .models import Contest

def save_contests(contests):
    for contest in contests:
        Contest.objects.update_or_create(
            platform=contest["platform"],
            contest_id=contest["contest_id"],
            defaults={
                "name": contest["name"],
                "url": contest["url"],
                "start_time": contest["start_time"],
                "duration_minutes": contest["duration_minutes"],
            },
        )