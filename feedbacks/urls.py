from django.urls import path
from django.views.generic import TemplateView

from feedbacks import views


app_name = 'feedbacks'
urlpatterns = [
    path('create/', views.feedback_create, name='create'),
    path('created/', TemplateView.as_view(
        template_name='feedbacks/feedback_created.html'), name='created'),
]
