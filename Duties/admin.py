from django.contrib import admin
from . models import Task, CheckList, Feedback, OldTaskCheckList, References, Quran_References

admin.site.register(Task)
admin.site.register(CheckList)
admin.site.register(Feedback)
admin.site.register(OldTaskCheckList)
admin.site.register(References)
admin.site.register(Quran_References)
