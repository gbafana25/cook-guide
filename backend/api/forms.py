from django import forms

class SearchForm(forms.Form):
	searchTerm = forms.CharField()
	numResults = forms.CharField()
	apiKey = forms.CharField(required=False)
