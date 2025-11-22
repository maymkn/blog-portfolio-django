from django import forms
import datetime
from .models import Achievement, Project, Experience, Skill, PortfolioItem

class PortfolioItemForm(forms.ModelForm):
    class Meta:
        model = PortfolioItem
        fields = '__all__'
        widgets = {
            "date_achieved": forms.DateInput(attrs={"type": "date"}),
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }

#A custom widget so I don't have to type it every time
class DateInput(forms.DateInput):
    input_type = 'date'


class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        fields = '__all__'
        widgets = {
            'date_achieved': DateInput(attrs={'max': datetime.date.today()}),
        }

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'start_date': DateInput(attrs={'max': datetime.date.today()}),
            'end_date': DateInput(),
        }

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = '__all__'
        widgets = {
            'start_date': DateInput(attrs={'max': datetime.date.today()}),
            'end_date': DateInput(attrs={'max': datetime.date.today()}),
        }

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'

#don't delete the date widgets. form submission will fail silently. took me 4 hours to figure out