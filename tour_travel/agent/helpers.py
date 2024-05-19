from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


def validate_user(**kwargs):
    username = kwargs.get('username')
    email = kwargs.get('email')
    errors = []

    user = User.objects
    if user.filter(username=username).exists():
        errors.append(_("A user with username already exists"))
    if user.filter(email=email).exists():
        errors.append(_("A user with username already exists"))

    return errors