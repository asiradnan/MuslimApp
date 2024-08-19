from django.urls import path
from . import views

urlpatterns = [
    path("tasks",views.task_list,name="task_list"),
    path("task/<int:id>/",views.task,name="task"),
    path("task_add/",views.task_add,name="task_add"),
    path("task_update/<int:id>/",views.task_update,name="task_update"),
    
    path("mytask/",views.mytask,name="mytask"),
    path("done/<int:id>",views.done,name="done"),
]