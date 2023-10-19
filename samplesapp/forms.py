from django import forms
from . models import SamplesModel, SampleUsageModel

class SamplesForm(forms.ModelForm):

    sample_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full border rounded bg-blue-200', "placeholder": "Pole wymagane np: Kora, ketamina"}))
    species = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full border rounded bg-blue-200', "placeholder": "np: mysz"}))
    sample_type = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full border rounded bg-blue-200', "placeholder": "np: Kora"}))
    owner = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full border rounded bg-blue-200 w-1/10', "placeholder": "Pole opcjonalne np: Bartek"}), required=False)
    location = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full border rounded bg-blue-200', "placeholder": "Pole wymagane np: -80, dolna półka"}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'w-full border rounded bg-blue-200', 'rows': '4', "placeholder": "Pole opcjonalne np: Próbki na proteomikę"}), required=False) 
    quantity = forms.IntegerField(
    widget=forms.NumberInput(attrs={'class': 'w-full border rounded bg-blue-200', 'step': '0.01'}),
    initial=1,  
)


    def __init__(self, *args, **kwargs):
        super(SamplesForm, self).__init__(*args, **kwargs)
        
        # Sprawdzanie, czy mamy instancję (czyli edytujemy obiekt)
        if self.instance and self.instance.pk:
            # Ustawiamy domyślną wartość dla 'quantity' na wartość z instancji
            self.initial['quantity'] = self.instance.quantity
            del self.fields['quantity']
            
            # Dodajemy logikę dla pola 'remained'
            self.initial['remained'] = self.instance.remained
            del self.fields['remained']
    
    class Meta:
        model = SamplesModel
        fields = '__all__'

class SampleUsageForm(forms.ModelForm):
    used_amount = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'text-center', 'step': '1'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'w-full border rounded', 'rows': '4', "placeholder": "Opis użycia próbki"}), required=False) 

    class Meta:
        model = SampleUsageModel
        fields = ['used_amount', 'description']