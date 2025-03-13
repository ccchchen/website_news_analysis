from django.urls import path
from app_news_sentiment import views

app_name = 'namespace_news_sentiment'

urlpatterns = [
    path('', views.home, name='home'),
    path('api_get_sentiment/', views.api_get_sentiment),
]
