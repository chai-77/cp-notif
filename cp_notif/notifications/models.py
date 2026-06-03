from django.db import models
# import contest model
from contests.models import Contest

# Create your models here.

class Notification(models.Model):
    contest = models.ForeignKey(Contest,on_delete=models.CASCADE)
    stage = models.CharField(max_length=10)  # "7d", "2d", "1h"
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["contest", "stage"],
                name="unique_contest_stage"
            )
        ]