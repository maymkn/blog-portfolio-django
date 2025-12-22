from django import forms
import datetime
from .models import PortfolioItem

class PortfolioItemForm(forms.ModelForm):
    class Meta:
        model = PortfolioItem
        fields = '__all__'
        widgets = {
            "date_achieved": forms.DateInput(attrs={"type": "date"}),
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }

