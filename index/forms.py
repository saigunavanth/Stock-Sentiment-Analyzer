from django import forms

class testp(forms.Form):
    text = forms.CharField(max_length=200)
    
class news_company(forms.Form):
    text = forms.CharField(max_length=200)