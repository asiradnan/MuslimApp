from django.db import models
from django.contrib.auth.models import User

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

    def __str__(self):
        return self.title
    
class CheckList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    taskID = models.ForeignKey(Task, on_delete=models.CASCADE)
    last_done = models.DateTimeField() 

class References(models.Model):
    taskID = models.ForeignKey(Task, on_delete=models.CASCADE)
    book = models.CharField(max_length=150)
    number = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.book}, {self.number}"

class Feedback(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    detail = models.CharField(max_length=1000)
    book = models.CharField(max_length=150)
    number = models.PositiveIntegerField()





    
