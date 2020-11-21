from django import forms
from .models import HealthModel

class HealthForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['max_temp'].widget = forms.HiddenInput()
        self.fields['weather'].widget = forms.HiddenInput()


    class Meta:
        model = HealthModel
        fields = ('max_temp', 'weather', 'condition', 'input_date', 'action')