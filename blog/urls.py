from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.PublicPostIndexView.as_view(), name='public_list'),
    path('private', views.PrivatePostIndexView.as_view(), name='private_list'),
    path('detail/<int:pk>/', views.PostDetailView.as_view(), name='detail'),
    path('comment/<int:pk>', views.CommentCreateView.as_view(), name='comment_create'),
    path('reply/create/<int:pk>/', views.ReplyCreate.as_view(), name='reply_create'),
    path('tag/list/<int:pk>/', views.TagView.as_view(), name='tag_search'),
]
