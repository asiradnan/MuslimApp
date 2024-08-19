from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Task, CheckList
from .serializers import TaskSerializer
from rest_framework import status
from django.utils import timezone


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

@api_view(["GET"])
def done(request, id):
    if request.user.is_authenticated:
        task = Task.objects.get(id=id)
        taskcheck,ok = CheckList.objects.get_or_create(task=task,user=request.user,date=timezone.now().date())
        if ok==False: 
            taskcheck.freqency+=1
            taskcheck.save()
        return Response({"Success":"Completed the task"})
    else: 
        return Response({"Error":"Please Log In first!"},status = status.HTTP_401_UNAUTHORIZED)
    