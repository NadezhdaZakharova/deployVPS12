from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from shop.api import api
from shop.views import (
    home, products_partial, export_catalog,
    demo_serialization, demo_serialization_wrong, demo_serialization_ok,
)

urlpatterns = [
    path("", home, name="home"),
    path("partials/products/", products_partial),
    path("api/", api.urls),
    path("export-catalog/", export_catalog, name="export_catalog"),
    path("demo-serialization/", demo_serialization, name="demo_serialization"),
    path("demo-serialization/wrong/", demo_serialization_wrong, name="demo_serialization_wrong"),
    path("demo-serialization/ok/", demo_serialization_ok, name="demo_serialization_ok"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)