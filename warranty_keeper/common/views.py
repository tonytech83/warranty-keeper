from collections import OrderedDict
from datetime import date

from django.views import generic as views

from warranty_keeper.suppliers.models import Supplier
from warranty_keeper.warranties.models import Warranty


class HomePageView(views.TemplateView):
    template_name = "common/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()

        warranties = list(
            Warranty.objects.filter(deleted=False).select_related("supplier")
        )

        active = [w for w in warranties if not w.is_expired]
        expired = [w for w in warranties if w.is_expired]

        # Non-overlapping urgency buckets among active warranties.
        expiring_30 = [w for w in active if w.days_before_expiration <= 30]
        healthy = [w for w in active if w.days_before_expiration > 30]

        # Spend totals.
        total_spend = sum((w.price or 0) for w in warranties)

        # Per-supplier counts and spend (ordered by number of warranties).
        count_by_supplier = {}
        spend_by_supplier = {}
        for w in warranties:
            name = w.supplier.name if w.supplier else "No supplier"
            count_by_supplier[name] = count_by_supplier.get(name, 0) + 1
            spend_by_supplier[name] = spend_by_supplier.get(name, 0) + (w.price or 0)

        supplier_labels = sorted(
            count_by_supplier, key=lambda n: count_by_supplier[n], reverse=True
        )

        # Expirations over the next 12 months (active warranties only).
        months = OrderedDict()
        for i in range(12):
            month = (today.month - 1 + i) % 12 + 1
            year = today.year + (today.month - 1 + i) // 12
            months[date(year, month, 1).strftime("%b %Y")] = 0
        for w in active:
            label = w.warranty_expiration_date.strftime("%b %Y")
            if label in months:
                months[label] += 1

        # Lists for the alert/activity panels.
        expiring_soon = sorted(
            [w for w in active if w.days_before_expiration <= 90],
            key=lambda w: w.days_before_expiration,
        )[:8]
        recent = sorted(warranties, key=lambda w: w.created_at, reverse=True)[:5]

        context.update(
            {
                # KPI cards
                "total_warranties": len(warranties),
                "total_suppliers": Supplier.objects.filter(deleted=False).count(),
                "active_count": len(active),
                "expiring_30_count": len(expiring_30),
                "expired_count": len(expired),
                "total_spend": total_spend,
                # Panels
                "expiring_soon": expiring_soon,
                "recent": recent,
                # Single payload rendered via one json_script tag and read by
                # staticfiles/js/dashboard.js (one tag keeps HTML formatters from
                # splitting it across lines and breaking the template).
                "chart_data": {
                    "status": {
                        "labels": ["Healthy", "Expiring ≤30 days", "Expired"],
                        "data": [len(healthy), len(expiring_30), len(expired)],
                    },
                    "supplier": {
                        "labels": supplier_labels,
                        "counts": [count_by_supplier[n] for n in supplier_labels],
                        "spend": [
                            float(spend_by_supplier[n]) for n in supplier_labels
                        ],
                    },
                    "timeline": {
                        "labels": list(months.keys()),
                        "data": list(months.values()),
                    },
                },
            }
        )
        return context
