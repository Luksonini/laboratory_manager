from django.urls import path
from . import views

app_name = "reagentsapp"

urlpatterns = [
    path("", views.reagents, name="reagents_list"),
    path('create_reagent/', views.create_reagent, name='create_reagent'),
    path('edit_reagent/<int:id>/', views.edit_reagent, name='edit_reagent'),
]