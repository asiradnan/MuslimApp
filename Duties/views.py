from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Task, CheckList, Feedback, OldTaskCheckList, Quran_References, References
from Leaderboards.models import PointTable
from Leaderboards.serializers import PointTableSerializer
from .serializers import TaskSerializer, FeedbackSerializer, TaskSerializer2, ReferencesSerializer, Quran_ReferencesSerializer
from rest_framework import status
from django.utils import timezone



def fard_percent_calc(user):
    muslim = user.muslim
    tasks_in_checklist = CheckList.objects.filter(user=user, date=timezone.now().date(),task__type="fard")
    if muslim.is_male:
        if muslim.is_married:
            objects  = Task.objects.filter(for_male = True, for_married = True, min_age__lte = muslim.age, type="fard")
        else:
            objects  = Task.objects.filter(for_male = True, for_unmarried = True, min_age__lte = muslim.age, type="fard")
    else:
        if muslim.is_married:
            objects  = Task.objects.filter(for_female = True, for_married = True, min_age__lte = muslim.age, type="fard")
        else:
            objects  = Task.objects.filter(for_female = True, for_unmarried = True, min_age__lte = muslim.age, type="fard")
    return len(tasks_in_checklist)/max(1,len(objects))*100

def sunnah_percent_calc(user):
    muslim = user.muslim
    tasks_in_checklist = CheckList.objects.filter(user=user, date=timezone.now().date(),task__type="sunnah")
    if muslim.is_male:
        if muslim.is_married:
            objects  = Task.objects.filter(for_male = True, for_married = True, min_age__lte = muslim.age, type="sunnah")
        else:
            objects  = Task.objects.filter(for_male = True, for_unmarried = True, min_age__lte = muslim.age, type="sunnah")
    else:
        if muslim.is_married:
            objects  = Task.objects.filter(for_female = True, for_married = True, min_age__lte = muslim.age, type="sunnah")
        else:
            objects  = Task.objects.filter(for_female = True, for_unmarried = True, min_age__lte = muslim.age, type="sunnah")
    return len(tasks_in_checklist)/max(1,len(objects))*100

@api_view(['GET'])
def task_list(request):
    if request.method == 'GET':
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    
@api_view(['GET'])
def task(request,id):
    task = Task.objects.get(id=id)
    serializer = TaskSerializer(task, many=False)
    return Response(serializer.data)
    
@api_view(['GET'])
def task_ref(request,id):
    task = Task.objects.get(id=id)
    references = References.objects.filter(taskID = task)
    Qreferences = Quran_References.objects.filter(taskID = task)
    serializer = TaskSerializer(task, many=False)
    ref_serializer = ReferencesSerializer(references, many = True)
    Qref_serializer = Quran_ReferencesSerializer(Qreferences, many = True)
    return Response({"quran_references":Qref_serializer.data,"hadith_references":ref_serializer.data})

@api_view(["GET"])
def mytask(request):
    if request.user.is_authenticated:
        muslim = request.user.muslim
        tasks_in_checklist = CheckList.objects.filter(user=request.user, date=timezone.now().date()).values_list('task', flat=True)
        if muslim.is_male:
            if muslim.is_married:
                objects  = Task.objects.filter(for_male = True, for_married = True, min_age__lte = muslim.age).exclude(id__in = tasks_in_checklist).order_by("priority")
                objects2  = Task.objects.filter(for_male = True, for_married = True, min_age__lte = muslim.age).filter(id__in = tasks_in_checklist).order_by("priority")
            else:
                objects  = Task.objects.filter(for_male = True, for_unmarried = True, min_age__lte = muslim.age).exclude(id__in = tasks_in_checklist).order_by("priority")
                objects2  = Task.objects.filter(for_male = True, for_unmarried = True, min_age__lte = muslim.age).filter(id__in = tasks_in_checklist).order_by("priority")
        else:
            if muslim.is_married:
                objects  = Task.objects.filter(for_female = True, for_married = True, min_age__lte = muslim.age).exclude(id__in = tasks_in_checklist).order_by("priority")
                objects2  = Task.objects.filter(for_female = True, for_married = True, min_age__lte = muslim.age).filter(id__in = tasks_in_checklist).order_by("priority")
            else:
                objects  = Task.objects.filter(for_female = True, for_unmarried = True, min_age__lte = muslim.age).exclude(id__in = tasks_in_checklist).order_by("priority")
                objects2  = Task.objects.filter(for_female = True, for_unmarried = True, min_age__lte = muslim.age).filter(id__in = tasks_in_checklist).order_by("priority")
        serializer = TaskSerializer(objects, many = True)
        points,ok = PointTable.objects.get_or_create(user=request.user,date=timezone.now().date()) 
        serializer2 = TaskSerializer(objects2, many = True)
        data = {"tasks":serializer.data, "completed_tasks":serializer2.data, "Current_Fard_Percent":points.fard_percent,"Current_Sunnah_Percent":points.sunnah_percent,"Current_Nafl_Points": points.nafl_points}
        return Response(data)
    else: 
        return Response({"Error":"Please Log In first!"},status = status.HTTP_401_UNAUTHORIZED)

@api_view(["GET"])
def done(request, id):
    if request.user.is_authenticated:
        task = Task.objects.get(id=id)
        taskcheck,ok = CheckList.objects.get_or_create(task=task,user=request.user,date=timezone.now().date())
        if ok == False: 
            taskcheck.frequency+=1
            taskcheck.save()
        points,ok = PointTable.objects.get_or_create(user=request.user,date=timezone.now().date()) 
        if task.type == "fard":
            points.fard_percent = fard_percent_calc(request.user)
            points.save()
            return Response({"Current_Fard_Percent":str(points.fard_percent)})
        elif task.type == "sunnah":
            points.sunnah_percent = sunnah_percent_calc(request.user)
            points.save()
            return Response({"Current_Sunnah_Percent":points.sunnah_percent})
        else: 
            points.nafl_points+=task.points
            points.save()
            return Response({"Current_Nafl_Points":str(points.nafl_points)})
    else: 
        return Response({"Error":"Please Log In first!"},status = status.HTTP_401_UNAUTHORIZED)
    
@api_view(["GET"])
def undo(request, id):
    if request.user.is_authenticated:
        task = Task.objects.get(id=id)
        taskcheck = CheckList.objects.get(task=task,user=request.user,date=timezone.now().date())
        points = PointTable.objects.get(user=request.user,date=timezone.now().date()) 
        taskcheck.delete()
        if task.type == "fard":
            points.fard_percent = fard_percent_calc(request.user)
            points.save()
            return Response({"Current_Fard_Percent":str(points.fard_percent)})
        elif task.type == "sunnah":
            points.sunnah_percent = sunnah_percent_calc(request.user)
            points.save()
            return Response({"Current_Sunnah_Percent":points.sunnah_percent})
        else: 
            points.nafl_points+=task.points
            points.save()
            return Response({"Current_Nafl_Points":str(points.nafl_points)})
    else: 
        return Response({"Error":"Please Log In first!"},status = status.HTTP_401_UNAUTHORIZED)

@api_view(["GET"])
def done_old(request, id, date):
    if request.user.is_authenticated:
        task = Task.objects.get(id=id)
        objects, ok = OldTaskCheckList.objects.get_or_create(user=request.user, task=task, task_date = date, done_date = timezone.now().date()) 
        if ok == False: 
            objects.frequency+=1
            objects.save()
        return Response({"Success":"Done bro"})
    else: 
        return Response({"Error":"Please Log In first!"},status = status.HTTP_401_UNAUTHORIZED)
    
@api_view(["GET"])
def undo_old(request, id, date):
    if request.user.is_authenticated:
        task = Task.objects.get(id=id)
        taskcheck = OldTaskCheckList.objects.get(task=task,user=request.user,task_date=date)
        taskcheck.delete()
        return Response({"Success":"Done"})
    else: 
        return Response({"Error":"Please Log In first!"},status = status.HTTP_401_UNAUTHORIZED)
    
@api_view(["GET"])
def get_history(request):
    if request.user.is_authenticated:
        objects = PointTable.objects.filter(user=request.user).order_by("-date")
        serializer = PointTableSerializer(objects,many = True)
        return Response(serializer.data)
    return Response({"Error":"Please Log In first!"},status = status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def history_detail(request,date):
    if request.user.is_authenticated:
        objects = CheckList.objects.filter(user = request.user,date=date).select_related('task').values('task__id', 'task__title','task__detail','task__type','task__priority')
        serializer = TaskSerializer2(objects,many = True)
        return Response(serializer.data)
    return Response({"Error":"Please Log In first!"},status = status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def history_detail_late(request,date):
    if request.user.is_authenticated:
        objects = OldTaskCheckList.objects.filter(user = request.user,task_date=date).select_related('task').values('task__id', 'task__title','task__detail','task__type','task__priority')
        serializer = TaskSerializer2(objects,many = True)
        return Response(serializer.data)
    return Response({"Error":"Please Log In first!"},status = status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def history_detail_incomplete(request,date):
    if request.user.is_authenticated:
        muslim = request.user.muslim
        tasks_in_checklist = CheckList.objects.filter(user=request.user, date=date).values_list('task', flat=True)
        tasks_in_oldchecklist = OldTaskCheckList.objects.filter(user=request.user, task_date=date).values_list('task', flat=True)
        if muslim.is_male:
            if muslim.is_married:
                objects  = Task.objects.filter(for_male = True, for_married = True, min_age__lte = muslim.age).exclude(id__in = tasks_in_checklist).exclude(id__in = tasks_in_oldchecklist).order_by("priority")
            else:
                objects  = Task.objects.filter(for_male = True, for_unmarried = True, min_age__lte = muslim.age).exclude(id__in = tasks_in_checklist).exclude(id__in = tasks_in_oldchecklist).order_by("priority")
        else:
            if muslim.is_married:
                objects  = Task.objects.filter(for_female = True, for_married = True, min_age__lte = muslim.age).exclude(id__in = tasks_in_checklist).exclude(id__in = tasks_in_oldchecklist).order_by("priority")
            else:
                objects  = Task.objects.filter(for_female = True, for_unmarried = True, min_age__lte = muslim.age).exclude(id__in = tasks_in_checklist).exclude(id__in = tasks_in_oldchecklist).order_by("priority")
        serializer = TaskSerializer(objects, many = True)
        return Response(serializer.data)
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