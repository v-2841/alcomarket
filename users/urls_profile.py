from django.urls import path

from users import views


app_name = 'profiles'
urlpatterns = [
    path('<str:username>/', views.profile, name='profile'),
    path('<str:username>/edit/', views.profile_edit, name='profile_edit'),
]
