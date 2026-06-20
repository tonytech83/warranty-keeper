from django.views import generic as views
from django.urls import reverse_lazy
from django.shortcuts import HttpResponseRedirect

from warranty_keeper.warranties.models import Warranty
from .forms import WarrantyCreateForm, WarrantyUpdateForm, WarrantyDeleteForm


class WarrantiesListView(views.ListView):
    model = Warranty
    template_name = "warranties/warranties-list.html"

    # ?status= values -> heading shown on the list page. Filtering happens in
    # Python because expiry is a computed property, not a database column.
    STATUS_LABELS = {
        "active": "Active warranties",
        "expiring": "Warranties expiring in ≤30 days",
        "expired": "Expired warranties",
    }

    def get_queryset(self):
        warranties = Warranty.objects.filter(deleted=False).select_related("supplier")
        status = self.request.GET.get("status")
        if status == "active":
            return [w for w in warranties if not w.is_expired]
        if status == "expired":
            return [w for w in warranties if w.is_expired]
        if status == "expiring":
            return [
                w
                for w in warranties
                if not w.is_expired and w.days_before_expiration <= 30
            ]
        return list(warranties)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_label"] = self.STATUS_LABELS.get(self.request.GET.get("status"))
        return context


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
    success_url = reverse_lazy("warranties-list")

    def get(self, request, *args, **kwargs):
        """Skip rendering the confirmation page and directly soft delete."""
        self.object = self.get_object()
        self.object.delete()  # Call the soft delete method
        return HttpResponseRedirect(self.success_url)