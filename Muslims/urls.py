from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("",views.list,name="list"),
    path("register",views.register,name="register"),
    path("login",views.login,name="login"),
    path("logout",views.log_out,name="logout"),
    path("loggedin",views.user_detail,name="user_detail"),
    path('refreshtoken', TokenRefreshView.as_view(), name='token_refresh'),
]