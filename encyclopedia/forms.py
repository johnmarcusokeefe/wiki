from django import forms

class SearchForm(forms.Form):
    get_search = forms.CharField(label='Get search')
    
    
class ContentForm(forms.Form): 
    title = forms.CharField(label = "Enter Title")
    content = forms.CharField(label = "Enter Content", widget=forms.Textarea)


class EditForm(forms.Form): 
    title = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    content = forms.CharField(label = "Edit Content", widget=forms.Textarea)
    