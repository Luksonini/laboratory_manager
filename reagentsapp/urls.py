from django.urls import path
from . import views

app_name = "reagentsapp"

urlpatterns = [
    path("", views.reagents, name="reagents_list"),
    path('create_reagent/', views.create_reagent, name='create_reagent'),
    path('edit_reagent/<int:id>/', views.edit_reagent, name='edit_reagent'),
    path('delete_reagent/<int:id>/', views.delete_reagent, name='delete_reagent'),
    path('reagent_detail/<int:id>/<str:access_key>/', views.reagent_details, name='reagent_details'),  
]