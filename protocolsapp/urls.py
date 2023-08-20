from django.urls import path
from . import views

app_name = "protocolsapp"

urlpatterns = [
    path("", views.protocols, name="protocols_list"), 
    path("protocol_detail/<int:id>", views.detail, name="protocol_detail"), 
]