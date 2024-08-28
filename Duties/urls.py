from django.urls import path
from . import views

urlpatterns = [
    path("tasks",views.task_list,name="task_list"),
    path("task/<int:id>/",views.task,name="task"),
    # path("task_add/",views.task_add,name="task_add"),
    # path("task_update/<int:id>/",views.task_update,name="task_update"),
    
    path("mytask/",views.mytask,name="mytask"),
    path("done/<int:id>",views.done,name="done"),
    path("undo/<int:id>",views.undo,name="undo"),
    path("compensate/<int:id>/<str:date>",views.compensate,name="compensate"),
    path("undocompensate/<int:id>/<str:date>",views.undo_compensate,name="undo_compensate"),
    path("history_detail/<str:date>",views.history_detail,name="history_detail"),
    path("history_detail_incomplete/<str:date>",views.history_detail_incomplete,name="history_detail_incomplete"),
    path("history_detail_late/<str:date>",views.history_detail_late,name="history_detail_late"),
    path("get_history",views.get_history,name="get_history"),
    path("feedback",views.feedback,name="feedback"),
]