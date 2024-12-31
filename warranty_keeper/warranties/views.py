from django.views import generic as views
from django.urls import reverse_lazy

from warranty_keeper.warranties.models import Warranty
from .forms import WarrantyCreateForm, WarrantyUpdateForm, WarrantyDeleteForm


class WarrantiesListView(views.ListView):
    model = Warranty
    template_name = "warranties/warranties-list.html"


class WarrantyDetailsView(views.DetailView):
    model = Warranty
    template_name = "warranties/details-warranty.html"


class WarrantyCreateView(views.CreateView):
    model = Warranty
    form_class = WarrantyCreateForm
    template_name = "warranties/create-warranty.html"
    success_url = reverse_lazy("warranties-list")


class WarrantyUpdateView(views.UpdateView):
    model = Warranty
    form_class = WarrantyUpdateForm
    template_name = "warranties/update-warranty.html"
    success_url = reverse_lazy("warranties-list")


class WarrantyDeleteView(views.DeleteView):
    model = Warranty
    form_class = WarrantyDeleteForm