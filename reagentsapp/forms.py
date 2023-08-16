from django import forms
from . models import Reagents

class ReagentForm(forms.ModelForm):
    reagent_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full', "placeholder": "Pole wymagane np: Fluoksetyna"}))
    expiration_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'w-full', 'type': 'date', "placeholder": "Pole opcjonalne"}), required=False)
    purchase_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'w-full', 'type': 'date', "placeholder": "Pole opcjonalne"}), required=False)
    owner = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full', "placeholder": "Pole opcjonalne np: Bartek"}), required=False)
    firm = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full',  "placeholder": "Pole opcjonalne np: Sigma"}), required=False)
    location = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full', "placeholder": "Pole wymagane np: lodówka w -6"}))
    cat_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full', "placeholder": "Pole opcjonalne np: PHR1394"}), required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'w-full', 'rows': '4', "placeholder": "Pole opcjonalne np: Odczynnik do grantu Berty"}), required=False) 

    class Meta:
        model = Reagents
        fields = ["reagent_name", "owner", "firm",
                   "location", "cat_number", "expiration_date", "purchase_date", "description"]


