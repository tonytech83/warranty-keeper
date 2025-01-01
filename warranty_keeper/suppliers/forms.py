from django import forms
from .models import Supplier


class SupplierBaseForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = "__all__"


class SupplierCreateForm(SupplierBaseForm):
    pass


class SupplierUpdateForm(SupplierBaseForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = False


class SupplierDeleteForm(SupplierBaseForm):
    pass
