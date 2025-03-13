from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic import TemplateView

urlpatterns = [
    # top keywords
    path('topword/', include('app_top_keyword.urls')),
    # top persons
    path('topperson/', include('app_top_person.urls')),
    # yesterday keywords
    path('topword_yesterday/', include('app_yesterday_top_keyword.urls')),
    # top ner
    path('topner/', include('app_top_ner.urls')),
    # keyword
    path('userkeyword/', include('app_user_keyword.urls')),
    # full text search and associated paragraphs for user keywords
    path('userkeyword_assoc/', include('app_user_key_ass.urls')),
    # news recommendation
    path('news_rcmd/', include('app_news_rcmd.urls')),
    # userkey sentiment
    path('sentiment/', include('app_userkey_sentiment.urls')),
    # leaderboard
    path('', include('app_leaderboard.urls')),
    # course introduction
    path('introduction', TemplateView.as_view(
        template_name='introduction.html'), name='course_introduction'),
    # delicious
    path('delicious', TemplateView.as_view(
        template_name='delicious.html'), name='delicious'),
    # Sentiment analysis
    path('news_sentiment/', include('app_news_sentiment.urls')),
    # news classification
    path('news_cate/', include('app_news_classify.urls')),



]
