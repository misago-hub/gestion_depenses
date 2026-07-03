from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


# =========================
# USER MANAGER
# =========================
class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError("Email obligatoire")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            **extra_fields
        )

        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "admin")
        extra_fields.setdefault("statut", "autorisé")

        return self.create_user(
            email,
            password,
            **extra_fields
        )


# =========================
# USER MODEL
# =========================
class User(AbstractUser):

    username = None

    nom = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    email = models.EmailField(
        unique=True
    )

    role = models.CharField(
        max_length=20,
        default="utilisateur"
    )

    statut = models.CharField(
        max_length=20,
        default="en attente"
    )

    # ==========================
    # PHOTO DE PROFIL
    # ==========================
    photo = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True,
        default="profiles/default.png"
    )

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email