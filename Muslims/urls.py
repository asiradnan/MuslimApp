from django.urls import path
from . import views

urlpatterns = [
    path("",views.list,name="list"),
    path("register",views.register,name="register"),
    path("login",views.login,name="login"),
    path("loggedin",views.loggedin,name="loggedin"),
]