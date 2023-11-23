from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('sobel', views.sobel, name="sobel"),
    path('median', views.median, name="median"),
    path('billateral', views.billateral, name='billateral'),
]

