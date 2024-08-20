from rest_framework import serializers
from .models import Task,CheckList

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Task
        fields = ["id","title","detail","type","points"]

class ChecklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckList
        fields = ['task',"date","freqency"]