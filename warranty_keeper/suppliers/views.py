from django.views import generic as views
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect


from warranty_keeper.suppliers.models import Supplier
from warranty_keeper.warranties.models import Warranty
from .forms import SupplierCreateForm, SupplierUpdateForm


class SupplierListView(views.ListView):
    model = Supplier
    template_name = "suppliers/suppliers-list.html"

    def get_queryset(self):
        return Supplier.objects.filter(deleted=False)


class SupplierDetailsView(views.DetailView):
    model = Supplier
    template_name = "suppliers/details-supplier.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        warranties = Warranty.objects.filter(
            supplier=self.object, deleted=False
        )
        # `is_expired` is a Python property, so split/sort in Python.
        context["active_warranties"] = sorted(
            (w for w in warranties if not w.is_expired),
            key=lambda w: w.days_before_expiration,
        )
        context["expired_warranties"] = sorted(
            (w for w in warranties if w.is_expired),
            key=lambda w: w.warranty_expiration_date,
            reverse=True,
        )
        return context


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
