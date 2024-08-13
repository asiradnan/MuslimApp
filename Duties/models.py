from django.db import models


task_type= [
    ("fard","Fard"),
    ("sunnah","Sunnah"),
    ("nafl","Nafl"),
]
class Task(models.Model):
    title = models.CharField(max_length=150)
    detail = models.CharField(max_length=300) #name
    type=models.CharField(choices=task_type,max_length=25)
    frequency  = models.PositiveIntegerField()
    points = models.IntegerField()
    


    
