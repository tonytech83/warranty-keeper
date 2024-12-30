from django.views import generic as views
from django.urls import reverse_lazy


from warranty_keeper.suppliers.models import Supplier
from .forms import SupplierCreateForm, SupplierUpdateForm, SupplierDeleteForm


class SupplierListView(views.ListView):
    model = Supplier
    template_name = "suppliers/suppliers-list.html"

class SupplierDetailsView(views.DetailView):
    model = Supplier
    template_name = "suppliers/details-supplier.html"


class SupplierCreateView(views.CreateView):
    model = Supplier
    form_class = SupplierCreateForm
    template_name = "suppliers/create-supplier.html"
    success_url = reverse_lazy("suppliers-list")


class SupplierUpdateView(views.UpdateView):
    model = Supplier
    form_class = SupplierUpdateForm
    template_name = "suppliers/update-supplier.html"
    success_url = reverse_lazy("suppliers-list")


class SupplierDeleteView(views.DeleteView):
    model = Supplier
    form_class = SupplierDeleteForm
