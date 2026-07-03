from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from accounts.models import User
from finance.models import Revenu, Transaction


# =====================================================
# 👥 LISTE UTILISATEURS (ADMIN)
# =====================================================
@login_required
def users_list(request):

    # =========================
    # SECURITE ADMIN
    # =========================
    if not request.user.is_superuser and request.user.role != "admin":
        return redirect("dashboard")

    # =========================
    # RECHERCHE
    # =========================
    search = request.GET.get("search")

    utilisateurs = User.objects.all().order_by("nom")

    if search:
        utilisateurs = utilisateurs.filter(
            email__icontains=search
        )

    # =========================
    # STATS ADMIN
    # =========================
    total_users = User.objects.count()
    users_actifs = User.objects.filter(statut="autorisé").count()
    users_suspendus = User.objects.filter(statut="suspendu").count()

    # =========================
    # DATA UTILISATEURS
    # =========================
    data = []

    for u in utilisateurs:

        revenus = Revenu.objects.filter(
            user=u
        ).aggregate(
            total=Sum("montant")
        )["total"] or 0

        depenses = Transaction.objects.filter(
            user=u
        ).aggregate(
            total=Sum("montant")
        )["total"] or 0

        solde = float(revenus) - float(depenses)

        data.append({
            "id": u.id,
            "nom": u.nom,
            "email": u.email,
            "role": u.role,
            "statut": u.statut,
            "revenus": revenus,
            "depenses": depenses,
            "solde": solde,
        })

    return render(request, "dashboard/users.html", {

        "utilisateurs": data,

        # stats
        "total_users": total_users,
        "users_actifs": users_actifs,
        "users_suspendus": users_suspendus,

    })


# =====================================================
# ✅ AUTORISER UTILISATEUR
# =====================================================
@login_required
def autoriser_user(request, pk):

    if not request.user.is_superuser and request.user.role != "admin":
        return redirect("dashboard")

    user = get_object_or_404(User, pk=pk)

    user.statut = "autorisé"
    user.save()

    return redirect("users_list")


# =====================================================
# ⛔ SUSPENDRE UTILISATEUR
# =====================================================
@login_required
def suspendre_user(request, pk):

    if not request.user.is_superuser and request.user.role != "admin":
        return redirect("dashboard")

    user = get_object_or_404(User, pk=pk)

    user.statut = "suspendu"
    user.save()

    return redirect("users_list")


# =====================================================
# 🗑 SUPPRIMER UTILISATEUR
# =====================================================
@login_required
def supprimer_user(request, pk):

    if not request.user.is_superuser and request.user.role != "admin":
        return redirect("dashboard")

    user = get_object_or_404(User, pk=pk)

    # éviter de supprimer soi-même
    if user != request.user:
        user.delete()

    return redirect("users_list")