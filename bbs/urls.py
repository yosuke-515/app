from django.urls import path
from . import views
from .models import Article
from django.views import generic

app_name = 'bbs'
 
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('create/', views.CreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.UpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.DeleteView.as_view(), name='delete'),
    path('comment/<int:pk>/', views.CommentCreate.as_view(), name='comment_create'),
    path('comment-delete/<int:pk>/<int:comment_pk>/', views.delete_comment, name='delete_comment'),
]