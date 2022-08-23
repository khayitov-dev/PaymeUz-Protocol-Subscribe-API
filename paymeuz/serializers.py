

from rest_framework import serializers


class SubscribeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    params = serializers.JSONField()