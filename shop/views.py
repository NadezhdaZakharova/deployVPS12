from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import VideoCard

def home(request):
    return render(request, "shop/home.html")


def products_partial(request):
    products = VideoCard.objects.all()
    return render(request, "shop/products_list.html", {"products": products})

def export_catalog(request):
    from shop.tasks import export_catalog_pdf
    """По нажатию кнопки ставит задачу и возвращает ответ."""
    from django_rq import get_queue
    queue = get_queue("default")
    queue.enqueue(export_catalog_pdf)
    if request.headers.get("HX-Request"):
        return render(request, "shop/components/export_status.html", {"message": "Экспорт запущен"})
    return redirect("home")
def demo_serialization(request):
    """Страница с двумя кнопками: неправильно / правильно."""
    product = VideoCard.objects.first()
    return render(request, "shop/demo_serialization.html", {"product": product})

@require_POST
def demo_serialization_wrong(request):
    """Передаём объект вместо id — будет ошибка сериализации."""
    from .tasks import export_product_pdf
    product = get_object_or_404(VideoCard, pk=request.POST.get("product_id"))
    export_product_pdf.enqueue(product)  # объект — ошибка!
    return redirect("demo_serialization")

@require_POST
def demo_serialization_ok(request):
    """Передаём id — правильно."""
    from .tasks import export_product_pdf
    product = get_object_or_404(VideoCard, pk=request.POST.get("product_id"))
    export_product_pdf.enqueue(product.id)  # id — ок
    if request.headers.get("HX-Request"):
        return render(request, "shop/components/demo_result.html", {"ok": True})
    return redirect("demo_serialization")