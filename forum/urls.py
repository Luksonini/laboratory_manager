
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "forum"

urlpatterns = [
    path("", views.index, name="index"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path('posts/', views.post_list, name='post-list'),
    path('posts/<int:id>/', views.post_update, name='post-update'),
    path('posts/<int:post_id>/like/', views.like_post, name='like-post'),
    path('posts/<int:post_id>/comments/', views.add_comment_to_post, name='add-comment-to-post'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)