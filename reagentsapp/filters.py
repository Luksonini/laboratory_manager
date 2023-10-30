import django_filters
from django import forms
from django_filters import CharFilter 
from .models import Reagents

class OrderFilter(django_filters.FilterSet):
    reagent_name = CharFilter(lookup_expr='icontains', widget=forms.TextInput(attrs={'class': 'form-input border rounded bg-blue-200', 'style': 'max-width: 100px;'}))
    owner = CharFilter(lookup_expr='icontains', widget=forms.TextInput(attrs={'class': 'form-input border rounded bg-blue-200', 'style': 'max-width: 100px;'}))
    firm = CharFilter(lookup_expr='icontains', widget=forms.TextInput(attrs={'class': 'form-input border rounded bg-blue-200', 'style': 'max-width: 100px;'}))
    location = CharFilter(lookup_expr='icontains', widget=forms.TextInput(attrs={'class': 'form-input border rounded bg-blue-200', 'style': 'max-width: 100px;'}))
    cat_number = CharFilter(lookup_expr='icontains', widget=forms.TextInput(attrs={'class': 'form-input border rounded bg-blue-200', 'style': 'max-width: 100px;'}))
    note = CharFilter(field_name="description", lookup_expr='icontains',
                       widget=forms.TextInput(attrs={'class': 'form-input border rounded bg-blue-200', 'style': 'max-width: 100px;'})
    )
    class Meta:
        model = Reagents
        fields = '__all__'
        exclude = ["purchase_date", "expiration_date", "description"]