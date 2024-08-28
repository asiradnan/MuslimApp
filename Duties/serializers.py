from rest_framework import serializers
from .models import Task,CheckList,Feedback


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Task
        fields = ["id","title","detail","type","points","priority"]

class TaskSerializer2(serializers.Serializer):
    task__id = serializers.IntegerField()
    task__title = serializers.CharField(max_length=150)
    task__detail = serializers.CharField(max_length=300) 
    task__type=serializers.CharField(max_length=25)
    task__priority=serializers.IntegerField()

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ["detail","book","number"]