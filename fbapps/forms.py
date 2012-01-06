from django import forms
from django.template import Template, TemplateSyntaxError

from models import FlatFacebookTab

class FlatFacebookTabForm(forms.ModelForm):
    def clean_content(self):
        content = self.cleaned_data.get('content', '')
        try:
            Template(content)
        except TemplateSyntaxError, e:
            raise forms.ValidationError(unicode(e))
        return content
    
    class Meta:
        model = FlatFacebookTab
