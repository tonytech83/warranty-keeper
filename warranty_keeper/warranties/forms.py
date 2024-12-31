from django import forms
from .models import Warranty

class WarrantyBaseForm(forms.ModelForm):
    class Meta:
        model = Warranty
        fields = "__all__"

class WarrantyCreateForm(WarrantyBaseForm):
    pass

class WarrantyUpdateForm(WarrantyBaseForm):
    pass

class WarrantyDeleteForm(WarrantyBaseForm):
    pass