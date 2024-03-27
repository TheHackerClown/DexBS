from django import forms


class Register(forms.Form):
    username = forms.CharField(max_length=20,label='',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'XD'}))
    desc = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'lorem ipsum'}))
    cover = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'form-control form-control-color','type':'color','id':'ColorInput'}))
class Create_Dex(forms.Form):
    name = forms.CharField(max_length=22,label='',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dex Name'}))
    dex = forms.CharField(max_length=22,label='',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'XD'}))
    propic = forms.FileField(widget=forms.FileInput(attrs={'accept':'image/*'}))
    cover = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'input form-control-color','type':'color','id':'Colorform-control'}))
    desc = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'lorem ipsum'}))
    rules = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': '1. rule \nrule 1 desc\n2. rule 2\nrule 2 desc   etc'}))

class Create_Post(forms.Form):
    title = forms.CharField(max_length=100,label='',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Post Title'}))
    file = forms.FileField(required=False,widget=forms.FileInput(attrs={'accept':'image/*,.mp4,.mp3'}))
    desc = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'lorem ipsum'}))

class Create_Comment(forms.Form):
    comment = forms.CharField(max_length=500,label='',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write your Comment','type':'text'}))

class VoteForm(forms.Form):
    vote_type = forms.ChoiceField(choices=[('upvote', 'Upvote'), ('downvote', 'Downvote')])
    post_id = forms.IntegerField(widget=forms.HiddenInput())