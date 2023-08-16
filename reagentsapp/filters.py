import django_filters
from django import forms
from django_filters import CharFilter 
from .models import Reagents

class OrderFilter(django_filters.FilterSet):
    reagent_name = CharFilter(widget=forms.TextInput(attrs={'class': 'form-input border rounded bg-blue-200'}))
    owner = CharFilter(widget=forms.TextInput(attrs={'class': 'form-input border rounded bg-blue-200'}))
    firm = CharFilter(widget=forms.TextInput(attrs={'class': 'form-input border rounded bg-blue-200'}))
    location = CharFilter(widget=forms.TextInput(attrs={'class': 'form-input border rounded bg-blue-200'}))
    cat_number = CharFilter(widget=forms.TextInput(attrs={'class': 'form-input border rounded bg-blue-200'}))
    note = CharFilter(field_name="description", lookup_expr='icontains',
                       widget=forms.TextInput(attrs={'class': 'form-input border rounded bg-blue-200'})
    )
    class Meta:
        model = Reagents
        fields = '__all__'
        exclude = ["purchase_date", "expiration_date", "description"]