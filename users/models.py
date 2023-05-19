from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class User(AbstractBaseUser, PermissionsMixin):
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "email",
    ]

    username = models.CharField(
        max_length=15,
        help_text=_("Required"),
        unique=True,
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(max_length=254, blank=False)
    last_name = models.CharField(max_length=254, blank=False)
    email = models.EmailField(_("email address"), blank=False)
    is_staff = models.BooleanField(
        default=False,
        help_text=_(
            "Whether the user is a Staff member or not. "
            "Controls whether the user can log into this admin site."
        ),
    )
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    objects = UserManager()
