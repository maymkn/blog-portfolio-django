from . import vn2_views
from django.urls import path


urlpatterns = [
    path("v2/portfolio/create/", vn2_views.CategorySelect_View.as_view(), name="select_category"),
    path("v2/portfolio/create/<str:category>/", vn2_views.PortfolioItemCreate_View.as_view(),
         name="create_portfolio_item"),
    #and you can now create your own paths for item details

]

#copy this and add it to the urlpatterns of the website urls: path("", inclue(portfolio.vn2_urls))
#now it will work