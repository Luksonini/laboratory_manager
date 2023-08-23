from django import forms
from . models import Protocols


    
class ProtocolsForm(forms.ModelForm):

    class Meta:
        model = Protocols
        fields = ["file"]



