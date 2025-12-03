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
