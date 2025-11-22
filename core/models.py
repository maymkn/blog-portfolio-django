from django.db import models

# Create your models here.
class SiteConfiguration(models.Model):
    site_name = models.CharField(max_length=200)
    tagline = models.TextField()
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    address = models.TextField()
    
class SocialMediaLink(models.Model):
    platform = models.CharField(max_length=50)
    url = models.URLField()
    icon_class = models.CharField(max_length=50)