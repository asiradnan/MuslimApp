from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Muslim(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    is_male = models.BooleanField()
    age=models.PositiveIntegerField()
    is_married = models.BooleanField()

    def __str__(self):
        return self.user.first_name+" "+self.user.last_name
