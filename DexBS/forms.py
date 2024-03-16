from django import forms

class SignUp(forms.Form):
    username = forms.CharField(max_length=20,label='',widget=forms.TextInput(attrs={'class': 'form-control hide-label', 'placeholder': 'XD'}))
    desc = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control hide-label', 'placeholder': 'lorem ipsum'}))
    cover = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'form-control hide-label form-control-color','type':'color','id':'ColorInput'}))