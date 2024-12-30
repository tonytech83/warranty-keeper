from django.urls import path

from warranty_keeper.warranties.views import WarrantiesListView

urlpatterns = (path("", WarrantiesListView.as_view(), name="warranties-list"),)
