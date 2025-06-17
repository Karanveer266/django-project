from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string

class User(AbstractUser):
    """
    – email must stay unique
    – username may be left blank by the registrant;
      we will auto-populate it right after the first save
    """
    email = models.EmailField(unique=True)

    username = models.CharField(
        max_length=150,
        unique=True,
        blank=True,          # user may omit it
        null=True,           # db allows NULL during first INSERT
    )

    USERNAME_FIELD  = "email"        # users still log in by email OR username
    REQUIRED_FIELDS = ['username']             # createsuperuser asks only for email+pwd

    def save(self, *args, **kwargs):
        """
        Two-phase save:
        1) insert row → pk generated
        2) if username is missing, set it to a slug based on pk
        """
        is_new = self.pk is None
        super().save(*args, **kwargs)          # phase-1: row exists, pk known

        if is_new and not self.username:       # phase-2: auto-fill once
            self.username = f"user_{self.pk}"
            # collision extremely unlikely, but guard anyway
            if User.objects.filter(username=self.username).exists():
                self.username = f"user_{self.pk}_{get_random_string(4)}"
            # save only that field to avoid recursion
            User.objects.filter(pk=self.pk).update(username=self.username)
