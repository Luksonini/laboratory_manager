from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "protocolsapp"

urlpatterns = [
    path("", views.protocols, name="protocols_list"),
    path("protocol_detail/<int:id>", views.detail, name="protocol_detail"),
    path('upload_and_process/', views.upload_and_process_protocol, name='upload_and_process_protocol'),
    path('delete_protocol/<int:id>/', views.delete_protocol, name='delete_protocol'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)