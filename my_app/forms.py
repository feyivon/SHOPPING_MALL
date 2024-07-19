from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price']

class ProductSearchForm(forms.Form):
    query = forms.CharField(max_length=100, label=False, 
                            widget = forms.TextInput(attrs={'class':'input-search',
                                                            'placeholder': 'search product..'}))
    