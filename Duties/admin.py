from django.contrib import admin
from . models import Task, CheckList, Feedback

admin.site.register(Task)
admin.site.register(CheckList)
admin.site.register(Feedback)