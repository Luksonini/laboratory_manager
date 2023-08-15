from django import forms
from . models import Reagents

class ReagentForm(forms.ModelForm):
    reagent_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full'}))
    expiration_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'w-full', 'type': 'date'}), required=False)
    purchase_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'w-full', 'type': 'date'}), required=False)
    owner = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full'}), required=False)
    firm = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full'}), required=False)
    location = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full'}))
    cat_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full'}), required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'w-full', 'rows': '4'}), required=False) 

    class Meta:
        model = Reagents
        fields = ["reagent_name", "owner", "firm",
                   "location", "cat_number", "expiration_date", "purchase_date", "description"]


