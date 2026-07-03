from django.db import models
from accounts.models import User


# ==================================================
# CATEGORIE
# ==================================================
class Categorie(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    nom = models.CharField(max_length=100)

    description = models.CharField(max_length=255, blank=True, null=True)

    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nom"]
        unique_together = ("user", "nom")

    def __str__(self):
        return self.nom


# ==================================================
# REVENUS (FONDS)
# ==================================================
class Revenu(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    source = models.CharField(max_length=150)

    montant = models.DecimalField(max_digits=12, decimal_places=2)

    description = models.TextField(blank=True, null=True)

    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.source} - {self.montant} FBu"


# ==================================================
# TRANSACTIONS (DEPENSES / RETRAITS)
# ==================================================
class Transaction(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    montant = models.DecimalField(max_digits=12, decimal_places=2)

    description = models.TextField(blank=True, null=True)

    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"Dépense - {self.montant} FBu"


# ==================================================
# BUDGET
# ==================================================
class Budget(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)

    montant = models.DecimalField(max_digits=12, decimal_places=2)

    mois = models.PositiveIntegerField()

    annee = models.PositiveIntegerField()

    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["annee", "mois"]
        unique_together = ("user", "categorie", "mois", "annee")

    def __str__(self):
        return f"{self.categorie} ({self.mois}/{self.annee})"


# ==================================================
# NOTIFICATIONS
# ==================================================
class Notification(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    titre = models.CharField(max_length=200)

    message = models.TextField()

    lu = models.BooleanField(default=False)

    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return self.titre