from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Task, CheckList, Feedback
from Leaderboards.models import PointTable
from .serializers import TaskSerializer, ChecklistSerializer, FeedbackSerializer
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

@api_view(["GET"])
def mytask(request):
    if request.user.is_authenticated:
        muslim = request.user.muslim
        tasks_in_checklist = CheckList.objects.filter(user=request.user, date=timezone.now().date()).values_list('task', flat=True)
        if muslim.is_male:
            if muslim.is_married:
                objects  = Task.objects.filter(for_male = True, for_married = True, min_age__lte = muslim.age).exclude(id__in = tasks_in_checklist).order_by("priority")
            else:
                objects  = Task.objects.filter(for_male = True, for_unmarried = True, min_age__lte = muslim.age).exclude(id__in = tasks_in_checklist).order_by("priority")
        else:
            if muslim.is_married:
                objects  = Task.objects.filter(for_female = True, for_married = True, min_age__lte = muslim.age).exclude(id__in = tasks_in_checklist).order_by("priority")
            else:
                objects  = Task.objects.filter(for_female = True, for_unmarried = True, min_age__lte = muslim.age).exclude(id__in = tasks_in_checklist).order_by("priority")
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
            taskcheck.frequency+=1
            taskcheck.save()
        pointobject,ok = PointTable.objects.get_or_create(user=request.user,date=timezone.now().date()) 
        pointobject.points+=task.points
        pointobject.save()
        return Response({"Success":"Completed the task"})
    else: 
        return Response({"Error":"Please Log In first!"},status = status.HTTP_401_UNAUTHORIZED)
    
@api_view(['GET'])
def myhistory(request):
    if request.user.is_authenticated:
        objects = CheckList.objects.filter(user = request.user)
        serializer = ChecklistSerializer(objects,many = True)
        data = {}
        for item in serializer.data:
            if item['date'] in data:
                data[item['date']].append(item)
            else:
                data[item['date']]=[item]
        return Response(data)
    return Response({"Error":"Please Log In first!"},status = status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def feedback(request):
    if request.user.is_authenticated:
        serializer = FeedbackSerializer(data = request.data)
        if serializer.is_valid():
            x = Feedback.objects.create(sender = request.user, detail = request.data['detail'],book = request.data['book'],number = request.data['number'])
            x.save()
            return Response({"Success":"Feedback received!"})
    return Response({"Error":"Please Log In first!"},status = status.HTTP_401_UNAUTHORIZED)
    














# @api_view(['POST'])
# def task_add(request):
#     serializer = TaskSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)

# @api_view(['POST'])
# def task_update(request,id):
#     task = Task.objects.get(id=id)
#     serializer = TaskSerializer(instance=task,data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)