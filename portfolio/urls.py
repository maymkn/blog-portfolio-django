from django.urls import path
from .views import (CategorySelectView, PortfolioItemCreateView, 
                    portfolio, PortfolioItemDetailView)


urlpatterns = [
    path("portfolio/", portfolio , name="portfolio-home"),

    path("portfolio/create/", CategorySelectView.as_view(), name="portfolio_category_select"),
    path("portfolio/create/<str:category>/", PortfolioItemCreateView.as_view(), name="portfolio_item_create"),
    path("portfolio/<int:pk>/", PortfolioItemDetailView.as_view(), name="portfolio_item_detail"),
]
