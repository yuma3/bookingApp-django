from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.IconList.as_view(), name='icon_list'),
]
