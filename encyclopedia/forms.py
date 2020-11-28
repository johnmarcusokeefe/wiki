from django import forms

class SearchForm(forms.Form):
    get_search = forms.CharField(label='Get search')
    
    
class ContentForm(forms.Form): 
    title = forms.CharField(label = "Enter Title")
    content = forms.CharField(label = "Enter Content", widget=forms.Textarea)