from django import forms
import requests,json,re

from ergo.validators import validate_address
from .models import wallet
from django.core.validators import RegexValidator

class WalletLookupModelForm(forms.ModelForm):
    address = forms.CharField(
        max_length=900, 
        
        validators=[validate_address]
        
        
        )

    print('hehheeh')
    class Meta:
        model = wallet
        fields = ['address']

    def get_add(self):
        cleaned_data= self.clean()
        print('is this running')
        return cleaned_data.get('address')
        
    




    def clean_title(self,*args, **kwargs):

        instance = self.instance

        address = self.cleaned_data.get('address')


        return address
    



   

    







