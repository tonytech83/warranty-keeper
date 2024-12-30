from django import forms
from .models import Supplier

class SupplierBaseForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = "__all__"

class SupplierCreateForm(SupplierBaseForm):
    pass

class SupplierUpdateForm(SupplierBaseForm):
    pass

class SupplierDeleteForm(SupplierBaseForm):
    pass