from django import forms
from .models import Warranty
from warranty_keeper.suppliers.models import Supplier
from warranty_keeper.warranties.models import Period


class WarrantyBaseForm(forms.ModelForm):
    class Meta:
        model = Warranty
        fields = "__all__"


class WarrantyCreateForm(WarrantyBaseForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add choices for Period
        self.fields["period"].choices = Warranty._meta.get_field("period").choices

        # Add choices for Supplier
        self.fields["supplier"].queryset = Supplier.objects.filter(
            deleted=False
        ).order_by("name")


class WarrantyUpdateForm(WarrantyBaseForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add choices for Period
        self.fields["period"].choices = Warranty._meta.get_field("period").choices

        # Add choices for Supplier
        self.fields["supplier"].queryset = Supplier.objects.filter(deleted=False)


class WarrantyDeleteForm(WarrantyBaseForm):
    pass
