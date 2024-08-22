from rest_framework import serializers
from .models import PointTable

class PointTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointTable
        fields = ["date","fard_percent","sunnah_percent","nafl_points"]