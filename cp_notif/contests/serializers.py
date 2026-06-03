from rest_framework import serializers
from .models import Contest

class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = ["contest_id", "id", "name", "platform", "start_time"]

