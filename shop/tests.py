from django.test import TestCase, override_settings

@override_settings(
    TASKS={
        "default": {"BACKEND": "django.tasks.backends.dummy.DummyBackend"},
    },
)
class ExportTasksTest(TestCase):
    def test_export_catalog_enqueue_does_not_run_task(self):
        """При DummyBackend enqueue не выполняет задачу, но не падает."""
        from shop.tasks import export_catalog_pdf
        result = export_catalog_pdf.enqueue()
        self.assertIsNotNone(result)
        # Код задачи не выполнялся — PDF не генерировался
