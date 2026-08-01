from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_default_site(sender, **kwargs):
    from django.conf import settings
    if 'django.contrib.sites' in settings.INSTALLED_APPS:
        try:
            from django.contrib.sites.models import Site
            Site.objects.get_or_create(
                id=getattr(settings, 'SITE_ID', 1),
                defaults={'domain': 'algodsa.onrender.com', 'name': 'AlgoDSA'}
            )
        except Exception:
            pass


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'
    verbose_name = 'Users'

    def ready(self):
        post_migrate.connect(create_default_site, sender=self)

