from django.urls import path
from app_user_key_ass import views

app_name="app_user_key_ass"

urlpatterns = [

    path('', views.home, name='home'),
    path('api_get_userkey_associate/', views.api_get_userkey_associate),

]
