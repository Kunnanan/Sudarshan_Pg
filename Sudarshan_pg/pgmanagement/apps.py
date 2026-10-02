from django.apps import AppConfig


class PgmanagementConfig(AppConfig):

    default_auto_field = "django.db.models.BigAutoField"

    name = "pgmanagement"

    def ready(self):

        import pgmanagement.signals