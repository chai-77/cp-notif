from django.db import models
from django.utils import timezone

# Create your models here.

class Contest (models.Model): 
    PLATFORM_CHOICES = (
        ("codeforces", "Codeforces"),
        ("leetcode", "LeetCode"),
        ("codechef", "CodeChef"),
    )
    contest_id = models.CharField(max_length=255) 
    name = models.CharField(max_length=255)

    platform = models.CharField(
        max_length=50,
        choices=PLATFORM_CHOICES
    )
    start_time = models.DateTimeField()
    duration_minutes = models.IntegerField()
    url = models.URLField()

    notify = models.BooleanField(default=True)
    emailed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["platform", "contest_id"],
                name="unique_contest_platform"
            )
        ]

    def time_left_minutes(self):
        return int((self.start_time - timezone.now()).total_seconds() / 60)

    def __str__(self):
        return f"{self.platform} - {self.name}"
    


class ReminderRule(models.Model):
    contest = models.ForeignKey("Contest", on_delete=models.CASCADE)

    # when to send reminder (in minutes before contest starts)
    offset_minutes = models.IntegerField()

    label = models.CharField(max_length=20)  # "4d", "1h"

    def __str__(self):
        return f"{self.contest} - {self.label}"