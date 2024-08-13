from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer



@api_view(['GET'])
def task_list(request):
    if request.method == 'GET':
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    
@api_view(['GET'])
def task(request,id):
    if request.method == 'GET':
        task = Task.objects.get(id=id)
        serializer = TaskSerializer(task, many=False)
        return Response(serializer.data)

@api_view(['POST'])
def task_add(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def task_update(request,id):
    task = Task.objects.get(id=id)
    serializer = TaskSerializer(instance=task,data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)
