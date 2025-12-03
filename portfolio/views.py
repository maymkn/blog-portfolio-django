from django.views.generic import TemplateView, CreateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.shortcuts import render
from .models import PortfolioItem
from .forms import PortfolioItemForm
from django import forms


CATEGORY_MAP = {
    "achievement": {
        "value": PortfolioItem.Category.ACHIEVEMENT,
        "verbose": "Achievement"
    },
    "project": {
        "value": PortfolioItem.Category.PROJECT,
        "verbose": "Project"
    },
    "experience": {
        "value": PortfolioItem.Category.EXPERIENCE,
        "verbose": "Experience"
    },
    "skill": {
        "value": PortfolioItem.Category.SKILL,
        "verbose": "Skill"
    },
}

class CategorySelectView(LoginRequiredMixin, TemplateView):
    template_name = "portfolio/select_category.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["categories"] = CATEGORY_MAP
        return ctx

class PortfolioItemCreateView(LoginRequiredMixin, CreateView):
    model = PortfolioItem
    form_class = PortfolioItemForm
    template_name = "portfolio/create_portfolio_item.html"

    def dispatch(self, request, *args, **kwargs):
        self.category_key = kwargs.get("category").lower()

        if self.category_key not in CATEGORY_MAP:
            raise Http404("Unknown category")

        self.category_data = CATEGORY_MAP[self.category_key]
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        return {"category": self.category_data["value"]}

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        category = self.category_data["value"]

        # Hide irrelevant fields
        if category == PortfolioItem.Category.ACHIEVEMENT:
            for field in ["start_date", "end_date", "role", "organization"]:
                form.fields[field].widget = forms.HiddenInput()

        elif category == PortfolioItem.Category.PROJECT:
            for field in ["issuer", "date_achieved", "role", "organization"]:
                form.fields[field].widget = forms.HiddenInput()

        elif category == PortfolioItem.Category.EXPERIENCE:
            for field in ["issuer", "date_achieved"]:
                form.fields[field].widget = forms.HiddenInput()

        elif category == PortfolioItem.Category.SKILL:
            for field in ["issuer", "date_achieved", "start_date", "end_date", "role", "organization"]:
                form.fields[field].widget = forms.HiddenInput()

        # Lock the category field
        form.fields["category"].widget = forms.HiddenInput()

        return form

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["category"] = self.category_data["verbose"]
        return ctx

    def get_success_url(self):
        return reverse_lazy("portfolio_item_detail", kwargs={"pk": self.object.pk})


class PortfolioItemDetailView(DetailView):
    model = PortfolioItem
    template_name = "portfolio/item_detail.html"
    context_object_name = "item"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = context["item"]

        # Map each category to fields we want to display
        category_fields = {
            PortfolioItem.Category.ACHIEVEMENT: [
                ("Title", item.title),
                ("Issuer", item.issuer),
                ("Date Achieved", item.date_achieved),
                ("Image", item.image),
                ("Description", item.description),
            ],
            PortfolioItem.Category.PROJECT: [
                ("Title", item.title),
                ("Description", item.description),
                ("Image", item.image),
                ("Start Date", item.start_date),
                ("End Date", item.end_date),
            ],
            PortfolioItem.Category.EXPERIENCE: [
                ("Title", item.title),
                ("Organization", item.organization),
                ("Role", item.role),
                ("Image", item.image),
                ("Start Date", item.start_date),
                ("End Date", item.end_date),
            ],
            PortfolioItem.Category.SKILL: [
                ("Title", item.title),
                ("Description", item.description),
                ("Image", item.image),
            ],
        }

        context["fields"] = category_fields.get(item.category, [])
        return context

def portfolio(request):

    custom_categories = [
        ('all', 'All'),
        *PortfolioItem.Category.choices,  # Unpack model choices
    ]
    context = {'portfolio_items': PortfolioItem.objects.all(), 'categories': custom_categories}
     
    return render(request, 'portfolio/portfolio_page.html', context)