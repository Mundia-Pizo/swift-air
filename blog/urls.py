from django.urls import path
from .views import PostListView, PostDetailView, upload_image
urlpatterns=[
    path('blogs/',PostListView.as_view(), name='posts' ),
    path('upload/', upload_image, name='upload'),
    path('<str:slug>/detail', PostDetailView.as_view(), name="post-detail")
]