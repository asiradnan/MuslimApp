from rest_framework import serializers
from .models import Task,CheckList,Feedback

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Task
        fields = ["id","title","detail","type","points"]

class ChecklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckList
        fields = ["task","date","frequency"]

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ["detail","book","number"]