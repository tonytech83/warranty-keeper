from django.views import generic as views

from warranty_keeper.warranties.models import Warranty

class HomePageView(views.ListView):
    queryset = Warranty.objects.all()
    template_name = "common/dashboard.html"