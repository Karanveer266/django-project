from django import forms
from submit.models import Submission

class CodeSubmissionForm(forms.ModelForm):
    class Meta:
        model  = Submission
        fields = ["language", "code", "input_data"]

    LANGUAGE_CHOICES = [
        ("cpp",  "C++"),
        ("py",   "Python"),
        ("java", "Java"),
    ]

    language = forms.ChoiceField(choices=LANGUAGE_CHOICES)
