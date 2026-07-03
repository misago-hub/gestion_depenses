from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from finance.models import (
    Revenu,
    Transaction,
    Budget,
    Notification
)

from accounts.models import User


# =====================================================
# DASHBOARD UTILISATEUR
# =====================================================

@login_required
def dashboard(request):

    # ==========================
    # REVENUS
    # ==========================
    total_revenus = Revenu.objects.filter(
        user=request.user
    ).aggregate(
        total=Sum("montant")
    )["total"] or 0

    # ==========================
    # DEPENSES
    # ==========================
    total_depenses = Transaction.objects.filter(
        user=request.user
    ).aggregate(
        total=Sum("montant")
    )["total"] or 0

    # ==========================
    # SOLDE
    # ==========================
    solde = float(total_revenus) - float(total_depenses)

    # ==========================
    # DERNIERES TRANSACTIONS
    # ==========================
    transactions = Transaction.objects.filter(
        user=request.user
    ).order_by("-date")[:10]

    # ==========================
    # ALERTES BUDGET
    # ==========================
    alertes = []

    budgets = Budget.objects.filter(user=request.user)

    for budget in budgets:

        depense = Transaction.objects.filter(
            user=request.user,
            categorie=budget.categorie
        ).aggregate(
            total=Sum("montant")
        )["total"] or 0

        pourcentage = 0

        if budget.montant > 0:
            pourcentage = (float(depense) / float(budget.montant)) * 100

        alertes.append({

            "categorie": budget.categorie.nom,

            "budget": budget.montant,

            "depense": depense,

            "pourcentage": round(pourcentage, 1)

        })

    # ==========================
    # PIE CHART
    # ==========================
    categories = Transaction.objects.filter(
        user=request.user
    ).values(
        "categorie__nom"
    ).annotate(
        total=Sum("montant")
    ).order_by("-total")

    # ==========================
    # NOTIFICATIONS
    # ==========================
    notifications = Notification.objects.filter(
        user=request.user,
        lu=False
    ).count()

    return render(

        request,

        "dashboard/dashboard.html",

        {

            "fonds_total": total_revenus,

            "retraits_total": total_depenses,

            "solde_actuel": solde,

            "transactions": transactions,

            "alertes": alertes,

            "categories": categories,

            "notifications_non_lues": notifications,

        }

    )


# =====================================================
# DASHBOARD ADMIN
# =====================================================

@login_required
def admin_dashboard(request):

    if not request.user.is_superuser and request.user.role != "admin":
        return redirect("dashboard")

    total_users = User.objects.count()

    total_revenus = Revenu.objects.aggregate(
        total=Sum("montant")
    )["total"] or 0

    total_depenses = Transaction.objects.aggregate(
        total=Sum("montant")
    )["total"] or 0

    solde = float(total_revenus) - float(total_depenses)

    categories_chart = Transaction.objects.values(
        "categorie__nom"
    ).annotate(
        total=Sum("montant")
    ).order_by("-total")[:5]

    chart_data = {

        "revenus": float(total_revenus),

        "depenses": float(total_depenses)

    }

    return render(

        request,

        "dashboard/admin_dashboard.html",

        {

            "total_users": total_users,

            "revenus": total_revenus,

            "depenses": total_depenses,

            "solde": solde,

            "chart_data": chart_data,

            "categories_chart": categories_chart,

        }

    )