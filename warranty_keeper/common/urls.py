from django.urls import path

from warranty_keeper.common.views import HomePageView

urlpatterns = (
    path('', HomePageView.as_view(), name='home-page'),
)