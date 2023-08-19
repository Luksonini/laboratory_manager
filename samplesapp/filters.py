import django_filters
from django import forms
from django_filters import CharFilter, DateFilter 
from .models import SamplesModel

from datetime import datetime

class MonthYearFilter(django_filters.Filter):
    def filter(self, qs, value):
        if value:
            date_obj = datetime.strptime(value, "%Y-%m-%d").date()
            return qs.filter(sample_date__year=date_obj.year, sample_date__month=date_obj.month)
        return qs
    

class OrderSampleFilter(django_filters.FilterSet):
    sample_date = MonthYearFilter(widget=forms.DateInput(attrs={'class': 'form-input border rounded bg-blue-200', 'type': 'date', 'style': 'max-width: 100px;'}))
    sample_name = CharFilter(lookup_expr='icontains', widget=forms.TextInput(attrs={'class': 'form-input border rounded bg-blue-200', 'style': 'max-width: 100px;'}))
    owner = CharFilter(lookup_expr='icontains', widget=forms.TextInput(attrs={'class': 'form-input border rounded bg-blue-200', 'style': 'max-width: 100px;'}))
    location = CharFilter(lookup_expr='icontains', widget=forms.TextInput(attrs={'class': 'form-input border rounded bg-blue-200', 'style': 'max-width: 100px;'}))
    sample_type = CharFilter(lookup_expr='icontains', widget=forms.TextInput(attrs={'class': 'form-input border rounded bg-blue-200', 'style': 'max-width: 100px;'}))

    class Meta:
        model = SamplesModel
        fields = '__all__'
       