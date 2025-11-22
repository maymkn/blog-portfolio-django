#You don't need to open this file. It's useless. Only those who need a different implementation
#of the portfolio

#version 2 below. 
#Note: Both versions share the same CSS files

from django.views.generic import TemplateView, CreateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.shortcuts import render

#for v2
from .forms import AchievementForm, ProjectForm, ExperienceForm, SkillForm
"""
The first version makes it simple. One unified model for all the portfolio items
 
The second version uses different models for Project, Achievement, Skill and Experience. 
Great if your project is quite robust and each section needs a lot of customization.v1 if there's a lot of overlap. 
I recommend v1. One table to rule them all.
For a small website, go with version one. You can add a new category to CATEGORY_MAP
and then make the appropriate adjustments in the view.

If you're going with v2, then def portfolio(request) view  will need a little editing.
You'll fiugre that out. and each category would need its own item detail html.
And 4 more views for those. Unless you figure a way out.

urls for v2 begin with v2/portfolio/...
"""










#v2

_CATEGORY_MAP = {
    "achievement": {
        "form": AchievementForm,
        "verbose": "Achievement",
    },
    "project": {
        "form": ProjectForm,
        "verbose": "Project",
    },
    "experience": {
        "form": ExperienceForm,
        "verbose": "Experience",
    },
    "skill": {
        "form": SkillForm,
        "verbose": "Skill",
    },
}


class CategorySelect_View(LoginRequiredMixin, TemplateView):
    template_name = "portfolio/v2/__select_category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = _CATEGORY_MAP
        return context


#looks like individual templates will be needed for all the classes
class PortfoliotemDetail_View(DetailView):
    
    context_object_name = 'item'
    template_name = 'portfolio/v2/portfolio_item.html'
    pass

class PortfolioItemCreate_View(LoginRequiredMixin, CreateView):
    template_name = "portfolio/v2/__create_portfolio_item.html"

    def dispatch(self, request, *args, **kwargs):
        self.category = kwargs.get("category").lower()
        #whatever you do, don't remove the lower(). crucial!!

        if self.category not in _CATEGORY_MAP:
            raise Http404("Category does not exist")

        self.form_class = _CATEGORY_MAP[self.category]["form"]
        self.verbose_name = _CATEGORY_MAP[self.category]["verbose"]

        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self):
        return self.form_class

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["category"] = self.category
        ctx["category_verbose"] = self.verbose_name
        return ctx

    def get_success_url(self):
        return reverse_lazy('home')



def portfolio(request):

    context = {'portfolio_items'}
    
    return render(request, 'portfolio/portfolio_page.html', context)