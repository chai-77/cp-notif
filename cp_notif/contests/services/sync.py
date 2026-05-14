from contests.models import Contest


def sync_contests(contest_list):
    for c in contest_list:
        Contest.objects.update_or_create(
            platform=c["platform"],
            external_id=c["external_id"],
            defaults={
                "name": c["name"],
                "start_time": c["start_time"],
                "duration_minutes": c["duration_minutes"],
                "url": c["url"],
                "contest_type": c.get("contest_type"),
            }
        )