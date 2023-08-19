from django.urls import path
from . import views

app_name = "samplesapp"

urlpatterns = [
    path("", views.samples, name="samples_list"),
    path('create_sample/', views.create_sample, name='create_sample'),
    path('edit_sample/<int:id>/', views.edit_sample, name='edit_sample'),
    path('delete_sample/<int:id>/', views.delete_sample, name='delete_sample'),
    path('sample_detail/<int:id>/<str:access_key>/', views.sample_details, name='sample_details'),  
    ]