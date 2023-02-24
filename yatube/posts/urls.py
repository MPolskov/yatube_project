from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('index', views.index),
    path('group_list', views.group_list),
    path('group/<slug:slug>/', views.group_posts),
]
