from django.urls import path, include

from warranty_keeper.warranties.views import (
    WarrantiesListView,
    WarrantyCreateView,
    WarrantyDetailsView,
    WarrantyUpdateView,
    WarrantyDeleteView,
)

urlpatterns = (
    path("", WarrantiesListView.as_view(), name="warranties-list"),
    path("create/", WarrantyCreateView.as_view(), name="warranty-create"),
    path("<int:pk>/", include([
        path("details/", WarrantyDetailsView.as_view(), name="warranty-details"),
        path("update/", WarrantyUpdateView.as_view(), name="warranty-update"),
        path("delete/", WarrantyDeleteView.as_view(), name="warranty-delete"),
    ]))
)
