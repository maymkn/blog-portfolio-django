from django.db import models

class PortfolioItem(models.Model):
    class Category(models.TextChoices):
        ACHIEVEMENT = "ACHIEVEMENT", "Achievement"
        PROJECT = "PROJECT", "Project"
        EXPERIENCE = "EXPERIENCE", "Experience"
        SKILL = "SKILL", "Skill"

    category = models.CharField(
        max_length=20,
        choices=Category.choices
    )

    # Shared fields
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="portfolio/", blank=True, null=True)

    # Optional fields used depending on category
    issuer = models.CharField(max_length=200, blank=True)         # Achievement
    date_achieved = models.DateField(blank=True, null=True)       # Achievement

    start_date = models.DateField(blank=True, null=True)          # Project/Experience
    end_date = models.DateField(blank=True, null=True)            # Project/Experience

    role = models.CharField(max_length=150, blank=True)           # Experience
    organization = models.CharField(max_length=150, blank=True)   # Experience

    def __str__(self):
        return f"{self.get_category_display()}: {self.title}"
    














#don't check these. for v2 only. unless you want to use v2
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
urls for v2 begin with v2/portfolio/..."""


class Achievement(models.Model):
    title = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    date_achieved = models.DateField()
    image = models.ImageField(upload_to='achievements/', null=True, blank=True)

    def __str__(self):
        return self.title

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='projects/', null=True, blank=True)

    def __str__(self):
        return self.title
    
class Experience(models.Model):
    role = models.CharField(max_length=150)
    organization = models.CharField(max_length=150)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.role} at {self.organization}"


class Skill(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)

    def __str__(self):
        return self.name


#Dear future self, or any other maintainer: 
#When you add a new model here, make its form and then add the appropriate category
#credentials to the create view. I have saved you a lot of future headache. Thank me!




