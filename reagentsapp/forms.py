from django import forms
from . models import Reagents
from django.core.validators import MinValueValidator
from decimal import Decimal


class ReagentForm(forms.ModelForm):
    UNIT_CHOICES = (
        ('-', '-'),
        ('ml', 'ml'),
        ('ul', 'ul'),
        ('g', 'g'),
        ('mg', 'mg'),
        ('szt', 'sztuk'),
    )
    reagent_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full border rounded bg-blue-200', "placeholder": "Pole wymagane np: Fluoksetyna"}))
    expiration_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'w-full border rounded bg-blue-200', 'type': 'date', "placeholder": "Pole opcjonalne"}), required=False)
    purchase_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'w-full border rounded bg-blue-200', 'type': 'date', "placeholder": "Pole opcjonalne"}), required=False)
    owner = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full border rounded bg-blue-200', "placeholder": "Pole opcjonalne np: Bartek"}), required=False)
    firm = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full border rounded bg-blue-200',  "placeholder": "Pole opcjonalne np: Sigma"}), required=False)
    location = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full border rounded bg-blue-200', "placeholder": "Pole wymagane np: lodówka w -6"}))
    cat_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full border rounded bg-blue-200', "placeholder": "Pole opcjonalne np: PHR1394"}), required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'w-full border rounded bg-blue-200', 'rows': '4', "placeholder": "Pole opcjonalne np: Odczynnik do grantu Berty"}), required=False) 
    unit = forms.ChoiceField(choices=UNIT_CHOICES, widget=forms.Select(attrs={'class': 'rounded bg-blue-200'}))
    quantity = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'w-full border rounded bg-blue-200', 'step': '0.01'}),  
    )
    
    class Meta:
        model = Reagents
        fields = ["reagent_name", "owner", "firm", "location", "cat_number", 
                "expiration_date", "purchase_date", "description", "quantity", "unit"]


class ReagentUsageForm(forms.ModelForm):
    used_amount = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'text-center', 'step': '0.1'}))

    class Meta:
        model = Reagents
        fields = []