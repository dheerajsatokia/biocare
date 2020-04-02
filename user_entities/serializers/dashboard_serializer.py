from .. import models
from rest_framework import serializers


class CountingSerializer(serializers.Serializer):
    doctor = serializers.CharField()
    lab = serializers.CharField()
    chemist = serializers.CharField()


class DashBoardSerializer(serializers.Serializer):
    counts = CountingSerializer()

    class Meta:
        fields = ['counts']
