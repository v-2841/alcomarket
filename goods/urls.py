from django.urls import path

from goods import views


app_name = 'goods'
urlpatterns = [
    path('test/', views.test, name='test'),
    path('', views.index, name='index'),
    path('<int:good_id>/add/', views.add_to_cart, name='add'),
    path('<int:good_id>/remove/', views.remove_from_cart, name='remove'),
    path('<int:good_id>/check/', views.check_cart_status, name='check'),
    # path('goods/<int:good_id>/', views.good_detail, name='good_detail'),
]
