from django.views import generic as views
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect


from warranty_keeper.suppliers.models import Supplier
from .forms import SupplierCreateForm, SupplierUpdateForm


class SupplierListView(views.ListView):
    model = Supplier
    template_name = "suppliers/suppliers-list.html"

    def get_queryset(self):
        return Supplier.objects.filter(deleted=False)


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
    success_url = reverse_lazy("suppliers-list")

    def get(self, request, *args, **kwargs):
        """Skip rendering the confirmation page and directly soft delete."""
        self.object = self.get_object()
        self.object.delete()  # Call the soft delete method
        return HttpResponseRedirect(self.success_url)
