from django.urls import path

from goods import views


app_name = 'goods'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:good_id>/add/', views.add_to_cart, name='add'),
    path('<int:good_id>/remove/', views.remove_from_cart, name='remove'),
]
