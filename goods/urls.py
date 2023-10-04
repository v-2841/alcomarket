from django.urls import path
from django.views.generic import TemplateView

# from goods import views


app_name = 'goods'
urlpatterns = [
    path('', TemplateView.as_view(
        template_name='goods/index.html'), name='index'),
    # path('', views.index, name='index'),
    # path('goods/<int:good_id>/', views.good_detail, name='good_detail'),
]
