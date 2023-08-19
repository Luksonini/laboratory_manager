from django import forms
from . models import SamplesModel

class SamplesForm(forms.ModelForm):

    sample_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full border rounded bg-blue-200', "placeholder": "Pole wymagane np: Kora, ketamina"}))
    species = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full border rounded bg-blue-200', "placeholder": "np: mysz"}))
    sample_type = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full border rounded bg-blue-200', "placeholder": "np: Kora"}))
    owner = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full border rounded bg-blue-200 w-1/10', "placeholder": "Pole opcjonalne np: Bartek"}), required=False)
    location = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full border rounded bg-blue-200', "placeholder": "Pole wymagane np: -80, dolna półka"}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'w-full border rounded bg-blue-200', 'rows': '4', "placeholder": "Pole opcjonalne np: Próbki na proteomikę"}), required=False) 
    quantity = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'w-full border rounded bg-blue-200', 'step': '0.01'}),  
    )
    
    class Meta:
        model = SamplesModel
        fields = '__all__'

class SampleUsageForm(forms.ModelForm):
    used_amount = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'text-center', 'step': '0.1'}))

    class Meta:
        model = SamplesModel
        fields = []