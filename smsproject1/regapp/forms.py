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
        exclude={"sid", "fid", "sprogram", "sdept", "say", "syr", "ssem", "ccode", "section"}
        labels={"q1":"Question1", "q2":"Question2", "q3":"Question3", "q4":"Question4", "q5":"Question5", "fdb1":"Answer1", "fdb2":"Answer2", "fdb3":"Answer3", "fdb4":"Answer4", "fdb5":"Answer5"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set widgets for q1, q2, q3, q4, and q5 to ReadOnlyInput and add CSS class
        for field_name in ['q1', 'q2', 'q3', 'q4', 'q5']:
            self.fields[field_name].widget = forms.TextInput(attrs={
                'readonly': 'readonly',
                'class': 'readonly-field'
            })