from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework.routers import DefaultRouter


def confirmation_mail(user):
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject="YaMDb регистрация",
        message=f"Ваш код подтверждения: {confirmation_code}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )


class NoPutRouter(DefaultRouter):

    def get_method_map(self, viewset, method_map):
        bound_methods = super().get_method_map(viewset, method_map)

        if "put" in bound_methods.keys():
            bound_methods.pop("put", None)
        return bound_methods
