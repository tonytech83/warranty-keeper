from urllib.parse import urlencode

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

    # Clickable columns: ?sort= value -> (header label, key function). Sorting is
    # in Python so it also covers the computed columns (expiration, days left).
    # The None-first tuples keep blank price/supplier values grouped together.
    SORT_COLUMNS = (
        ("item", "Item", lambda w: w.item_name.lower()),
        ("purchase_date", "Purchase date", lambda w: w.purchase_date),
        ("period", "Period", lambda w: w.period),
        ("expiration", "Expiration date", lambda w: w.warranty_expiration_date),
        ("days_left", "Days left", lambda w: w.days_before_expiration),
        ("price", "Price", lambda w: (w.price is None, w.price or 0)),
        (
            "supplier",
            "Supplier",
            lambda w: (w.supplier is None, w.supplier.name.lower() if w.supplier else ""),
        ),
    )
    DEFAULT_SORT = "purchase_date"

    def _resolve_sort(self):
        """Return the (sort, direction) to apply, falling back to the defaults."""
        sort = self.request.GET.get("sort")
        if sort not in dict((c[0], c) for c in self.SORT_COLUMNS):
            sort = self.DEFAULT_SORT
        direction = self.request.GET.get("dir")
        if direction not in ("asc", "desc"):
            direction = "asc"  # default: oldest/smallest on top
        return sort, direction

    def get_queryset(self):
        warranties = list(
            Warranty.objects.filter(deleted=False).select_related("supplier")
        )
        status = self.request.GET.get("status")
        if status == "active":
            warranties = [w for w in warranties if not w.is_expired]
        elif status == "expired":
            warranties = [w for w in warranties if w.is_expired]
        elif status == "expiring":
            warranties = [
                w
                for w in warranties
                if not w.is_expired and w.days_before_expiration <= 30
            ]

        sort, direction = self._resolve_sort()
        key = next(c[2] for c in self.SORT_COLUMNS if c[0] == sort)
        warranties.sort(key=key, reverse=(direction == "desc"))
        return warranties

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        status = self.request.GET.get("status")
        context["filter_label"] = self.STATUS_LABELS.get(status)

        sort, direction = self._resolve_sort()
        columns = []
        for name, label, _ in self.SORT_COLUMNS:
            active = name == sort
            # Clicking the active column flips direction; others start ascending.
            next_dir = "desc" if active and direction == "asc" else "asc"
            params = {"sort": name, "dir": next_dir}
            if status:
                params["status"] = status
            columns.append(
                {
                    "label": label,
                    "href": "?" + urlencode(params),
                    "active": active,
                    "arrow": ("▲" if direction == "asc" else "▼") if active else "",
                }
            )
        context["columns"] = columns
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