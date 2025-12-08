# forms.py
from django import forms

# import the model for which the form is being created
from .models import UploadedImage

# form for uploading an image
class UploadImageForm(forms.ModelForm):
    name = forms.CharField(label='Name', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    image = forms.ImageField(label='Image', widget=forms.FileInput(attrs={'class': 'form-control-file'}))

    class Meta:
        model = UploadedImage # specify the model to be used
        fields = ['name', 'image']
