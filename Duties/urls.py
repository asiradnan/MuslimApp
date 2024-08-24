from django.urls import path
from . import views

urlpatterns = [
    path("tasks",views.task_list,name="task_list"),
    path("task/<int:id>/",views.task,name="task"),
    # path("task_add/",views.task_add,name="task_add"),
    # path("task_update/<int:id>/",views.task_update,name="task_update"),
    
    path("mytask/",views.mytask,name="mytask"),
    path("done/<int:id>",views.done,name="done"),
    path("done_old/<int:id>/<str:date>",views.done_old,name="done_old"),
    path("history_detail/<str:date>",views.history_detail,name="history_detail"),
    path("history_detail_incomplete/<str:date>",views.history_detail_incomplete,name="history_detail_incomplete"),
    path("get_history",views.get_history,name="get_history"),
    path("feedback",views.feedback,name="feedback"),
]