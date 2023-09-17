from django import forms

class SignupForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    mobile = forms.CharField(max_length=10)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)


from django import forms
from userapp.models import Product, CATEGORY_CHOICES

class ProductForm(forms.ModelForm):
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, initial='wheelchair')
    
    class Meta:
        model = Product
        fields = ['category', 'name', 'price', 'description', 'image']
        

class ProductUpdateForm(forms.ModelForm):
    category = forms.ChoiceField(choices=CATEGORY_CHOICES)
    
    class Meta:
        model = Product
        fields = ['category', 'name', 'price', 'description', 'image']



class DeleteProductForm(forms.Form):
    confirm = forms.BooleanField(
        label='Confirm Deletion', 
        required=True, 
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

