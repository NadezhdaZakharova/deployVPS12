import os
from django.conf import settings

def export_catalog_pdf() -> str:
    
    """Генерирует PDF-каталог товаров и сохраняет в media/exports/."""
    from .models import VideoCard
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas

    path = os.path.join(settings.MEDIA_ROOT, "exports", "catalog.pdf")
    os.makedirs(os.path.dirname(path), exist_ok=True)

    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    pdfmetrics.registerFont(TTFont("Calibri", "C:/Windows/Fonts/calibri.ttf"))

    c = canvas.Canvas(path, pagesize=A4)
    c.setFont("Calibri", 14)
    c.drawString(50, 800, "Каталог видеокарт")
    for i, p in enumerate(VideoCard.objects.all()):
        c.drawString(50, 770 - i * 20, f"{p.name} — {p.price:.0f} ₽")
    c.save()
    return path

def export_product_pdf(product_id: int) -> str:
    """Экспорт одного товара — пример задачи с аргументом."""
    from .models import VideoCard
    p = VideoCard.objects.get(pk=product_id)
    return f"ok: {p.name}"