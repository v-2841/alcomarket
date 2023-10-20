from django.urls import path

from goods import views


app_name = 'goods'
urlpatterns = [
    path('', views.index, name='index'),
    path('goods/<int:good_id>/', views.good_detail, name='good_detail'),
    path('goods/<int:good_id>/add/', views.add_to_cart, name='add'),
    path('goods/<int:good_id>/remove/', views.remove_from_cart, name='remove'),
    path('categories/', views.categories, name='categories'),
    path('category/<slug:slug>/', views.category_goods,
         name='category_goods'),
    path('manufacturers/', views.manufacturers, name='manufacturers'),
    path('manufacturer/<slug:slug>/', views.manufacturer_goods,
         name='manufacturer_goods'),
    path('search/', views.search, name='search'),
    path('shopping_cart/', views.shopping_cart, name='shopping_cart'),
    path('shopping_cart/<int:good_id>/remove/', views.shopping_cart_remove,
         name='shopping_cart_remove'),
    path('pre_order/', views.pre_order, name='pre_order'),
    path('ordered/', views.ordered, name='ordered'),
]
