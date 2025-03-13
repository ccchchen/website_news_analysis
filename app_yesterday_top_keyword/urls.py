from django.urls import path
from app_yesterday_top_keyword import views

# declare a  namespace for this APP
# the name of namespace is  'app_top_keyword'
# We will use the namespace in the future integrated website.
app_name = 'app_yesterday_top_keyword'

urlpatterns = [
    path('', views.chart_cate_topword_y, name='chart_topword_yesterday'),
    path('api_get_cate_topword_y/', views.api_get_cate_topword_y,
         name='api_cate_topword_y'),
]
