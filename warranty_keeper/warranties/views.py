from django.views import generic as views


from warranty_keeper.warranties.models import Warranty


class WarrantiesListView(views.ListView):
    model = Warranty
    template_name = "warranties/warranties-list.html"
