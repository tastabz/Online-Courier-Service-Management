from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    User app configuration class.

    :ivar name: Name of the app.
    :vartype name: str
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
