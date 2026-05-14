from django.db import models
from django.utils import timezone


class Contest(models.Model):
    PLATFORM_CHOICES = [
        ("codeforces", "Codeforces"),
        ("leetcode", "LeetCode"),
        ("atcoder", "AtCoder"),
    ]

    external_id = models.CharField(max_length=100)

    name = models.CharField(max_length=255)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)

    start_time = models.DateTimeField()
    duration_minutes = models.IntegerField()

    url = models.URLField()

    contest_type = models.CharField(max_length=50, null=True, blank=True)

    notify = models.BooleanField(default=True)
    emailed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["platform", "external_id"],
                name="unique_contest_platform_external"
            )
        ]

    def time_left_minutes(self):
        return int((self.start_time - timezone.now()).total_seconds() / 60)

    def __str__(self):
        return f"{self.platform} - {self.name}"


class ContestNotification(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    stage = models.CharField(max_length=10)  # "7d", "2d", "1h"
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("contest", "stage")