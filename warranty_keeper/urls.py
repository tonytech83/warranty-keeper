from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.views.decorators.clickjacking import xframe_options_sameorigin

from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('warranty_keeper.common.urls')),
    path('warranties/', include('warranty_keeper.warranties.urls')),
    path('suppliers/', include('warranty_keeper.suppliers.urls')),
]

# Serve user-uploaded media (invoices, logos). Done explicitly so it also works
# under DEBUG=False / Gunicorn in Docker, which is fine for a single-user app.
# xframe_options_sameorigin overrides the project-wide X-Frame-Options: DENY so a
# PDF invoice can be embedded (in <object>) on its own same-origin details page.
urlpatterns += [
    re_path(
        r'^media/(?P<path>.*)$',
        xframe_options_sameorigin(serve),
        {'document_root': settings.MEDIA_ROOT},
    ),
]
