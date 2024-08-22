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
    for_male = models.BooleanField()
    for_female = models.BooleanField()
    min_age = models.PositiveIntegerField()
    for_married = models.BooleanField()
    for_unmarried = models.BooleanField()
    points = models.IntegerField()
    priority = models.IntegerField()

    def __str__(self):
        return self.title
    
class CheckList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    date = models.DateField() 
    frequency = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " : " + self.task.title

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





    
