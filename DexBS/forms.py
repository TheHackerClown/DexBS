from django import forms

class Register(forms.Form):
    username = forms.CharField(max_length=20,label='',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'XD'}))
    desc = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'lorem ipsum'}))
    cover = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'form-control form-control-color','type':'color','id':'ColorInput'}))
class Create_Dex(forms.Form):
    name = forms.CharField(max_length=20,label='',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dex Name'}))
    dex = forms.CharField(max_length=20,label='',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'XD'}))
    propic = forms.ImageField(label="select Dex Profile pic")
    cover = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'input form-control-color','type':'color','id':'Colorform-control'}))
    desc = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'lorem ipsum'}))
    rule = forms.CharField(max_length=20,label='',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1. rule 1, 2. rule 2,'}))
    rule_desc = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': '1. rule desc, 2. rule desc'}))

class Create_Post(forms.Form):
    title = forms.CharField(max_length=20,label='',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Post Title'}))
    image = forms.ImageField(label="select a file",required=False)
    desc = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'lorem ipsum'}))

class Comment(forms.Form):
    comment = forms.CharField(max_length=500,label='',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write your Comment','type':'text'}))

class VoteForm(forms.Form):
    vote_type = forms.ChoiceField(choices=[('upvote', 'Upvote'), ('downvote', 'Downvote')])
    post_id = forms.IntegerField(widget=forms.HiddenInput())