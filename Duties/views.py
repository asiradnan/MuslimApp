from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
from rest_framework import status



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

@api_view(["GET"])
def mytask(request):
    if request.user.is_authenticated:
        muslim = request.user.muslim
        if muslim.is_male:
            if muslim.is_married:
                objects  = Task.objects.filter(for_male = True, for_married = True, min_age__lte = muslim.age)
            else:
                objects  = Task.objects.filter(for_male = True, for_unmarried = True, min_age__lte = muslim.age)
        else:
            if muslim.is_married:
                objects  = Task.objects.filter(for_female = True, for_married = True, min_age__lte = muslim.age)
            else:
                objects  = Task.objects.filter(for_female = True, for_unmarried = True, min_age__lte = muslim.age)
        serializer = TaskSerializer(objects, many = True)
        return Response(serializer.data)
    else: 
        return Response({"Error":"Please Log In first!"},status = status.HTTP_401_UNAUTHORIZED)