from django.urls import path, include

from warranty_keeper.suppliers.views import (
    SupplierListView,
    SupplierCreateView,
    SupplierDetailsView,
    SupplierUpdateView,
    SupplierDeleteView,
)

urlpatterns = (
    path("", SupplierListView.as_view(), name="suppliers-list"),
    path("create/", SupplierCreateView.as_view(), name="supplier-create"),
    path("<int:pk>/", include([
                path("details/", SupplierDetailsView.as_view(), name="supplier-details"),
                path("update/", SupplierUpdateView.as_view(), name="supplier-update"),
                path("delete/", SupplierDeleteView.as_view(), name="supplier-delete"),
    ]))
)
