from django import forms

from .models import RegM, FeedbackPosted
class AddRegForm(forms.ModelForm):
    class Meta:
        model=RegM
        fields="__all__"

class FeedbackForm(forms.ModelForm):
    class Meta:
        model=FeedbackPosted
        fields="__all__"
