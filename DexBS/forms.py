from django import forms

class Register(forms.Form):
    username = forms.CharField(max_length=20,label='',widget=forms.TextInput(attrs={'class': 'nes-input', 'placeholder': 'XD'}))
    desc = forms.CharField(widget=forms.Textarea(attrs={'class': 'nes-input', 'placeholder': 'lorem ipsum'}))
    cover = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'nes-input form-control-color','type':'color','id':'ColorInput'}))

class Search(forms.Form):
    search = forms.CharField(max_length=100,label='',widget=forms.TextInput(attrs={'class': 'nes-input', 'placeholder': 'Search','type':'search'}))

class Create_Dex(forms.Form):
    dex = forms.CharField(max_length=20,label='',widget=forms.TextInput(attrs={'class': 'nes-input', 'placeholder': 'XD'}))
    desc = forms.CharField(widget=forms.Textarea(attrs={'class': 'nes-input', 'placeholder': 'lorem ipsum'}))

class Create_Post(forms.Form):
    user = forms.CharField(max_length=20,label='',widget=forms.TextInput(attrs={'class': 'nes-input', 'placeholder': 'XD'}))
    desc = forms.CharField(widget=forms.Textarea(attrs={'class': 'nes-input', 'placeholder': 'lorem ipsum'}))

