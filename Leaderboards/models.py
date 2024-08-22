from django.db import models
from django.contrib.auth.models import User

class PointTable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    fard_percent = models.FloatField(default=0)
    sunnah_percent = models.FloatField(default=0)
    nafl_points = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'date')

class TrophyTable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length = 200)
