from django.urls import path
from . import views

app_name = "protocolsapp"

urlpatterns = [
    path("", views.protocols, name="protocols_list"), 
    path("protocol_detail/<int:id>", views.detail, name="protocol_detail"), 
    path('upload_and_process/', views.upload_and_process_protocol, name='upload_and_process_protocol'),
    path('delete_protocol/<int:id>/', views.delete_protocol, name='delete_protocol'),
]