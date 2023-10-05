from django.urls import path

from goods import views


app_name = 'goods'
urlpatterns = [
    path('test/', views.test, name='test'),
    path('', views.index, name='index'),
    # path('goods/<int:good_id>/', views.good_detail, name='good_detail'),
]
