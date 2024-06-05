from django import forms

from .models import RegM, FeedbackPosted
class AddRegForm(forms.ModelForm):
    class Meta:
        model=RegM
        fields="__all__"
        labels={"dept":"Department", "ay":"Academic Year", "yr":"Cycle", "sem":"Semester",
                "c1": "Course1", "f11":"Faculty1", "f12":"Faculty2", "f13":"Faculty3",
                "c2": "Course2", "f21":"Faculty1", "f22":"Faculty2", "f23":"Faculty3",
                "c3": "Course3", "f31":"Faculty1", "f32":"Faculty2", "f33":"Faculty3",
                "c4": "Course4", "f41": "Faculty1", "f42": "Faculty2", "f43": "Faculty3",
                "c5": "Course5", "f51": "Faculty1", "f52": "Faculty2", "f53": "Faculty3",
                "c6": "Course6", "f61": "Faculty1", "f62": "Faculty2", "f63": "Faculty3",
                "c7": "Course7", "f71": "Faculty1", "f72": "Faculty2", "f73": "Faculty3",
                }

class FeedbackForm(forms.ModelForm):
    class Meta:
        model=FeedbackPosted
        fields="__all__"
