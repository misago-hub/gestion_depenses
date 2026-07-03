from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse

from reportlab.pdfgen import canvas
from io import BytesIO

from django.core.mail import send_mail
from datetime import datetime

from .models import Revenu, Transaction, Categorie, Budget, Notification
# ==================================================
# DASHBOARD
# ==================================================
@login_required
def dashboard(request):

    total_revenus = Revenu.objects.filter(user=request.user).aggregate(
        total=Sum("montant")
    )["total"] or 0

    total_depenses = Transaction.objects.filter(user=request.user).aggregate(
        total=Sum("montant")
    )["total"] or 0

    solde = float(total_revenus) - float(total_depenses)

    return render(request, "dashboard/dashboard.html", {
        "total_revenus": total_revenus,
        "total_depenses": total_depenses,
        "solde": solde
    })


# ==================================================
# REVENUS
# ==================================================
@login_required
def revenu_list(request):

    revenus = Revenu.objects.filter(user=request.user).order_by("-date")

    total = revenus.aggregate(total=Sum("montant"))["total"] or 0

    # =========================
    # FORMAT PRO POUR UI
    # =========================
    data = []

    for r in revenus:
        data.append({
            "id": r.id,
            "date": r.date,
            "source": r.source,
            "montant": r.montant,
            "description": r.description
        })

    return render(request, "finance/revenus.html", {
        "revenus": data,
        "total": total
    })

@login_required
def add_revenu(request):

    categories = Categorie.objects.filter(user=request.user)

    if request.method == "POST":

        Revenu.objects.create(
            user=request.user,
            categorie_id=request.POST.get("categorie"),
            source=request.POST.get("source"),
            montant=request.POST.get("montant"),
            description=request.POST.get("description"),
        )

        return redirect("revenu_list")

    return render(request, "finance/add_revenu.html", {
        "categories": categories
    })


@login_required
def delete_revenu(request, pk):

    revenu = get_object_or_404(Revenu, pk=pk, user=request.user)
    revenu.delete()

    return redirect("revenu_list")


# ==================================================
# TRANSACTIONS
# ==================================================
@login_required
def transaction_list(request):

    transactions = Transaction.objects.filter(user=request.user)

    total_depenses = transactions.aggregate(total=Sum("montant"))["total"] or 0

    return render(request, "finance/transactions.html", {
        "transactions": transactions,
        "total_depenses": total_depenses
    })


@login_required
def add_transaction(request):

    categories = Categorie.objects.filter(user=request.user)

    if request.method == "POST":

        Transaction.objects.create(
            user=request.user,
            categorie_id=request.POST.get("categorie"),
            montant=request.POST.get("montant"),
            description=request.POST.get("description")
        )

        return redirect("transaction_list")

    return render(request, "finance/add_transaction.html", {
        "categories": categories
    })


@login_required
def delete_transaction(request, pk):

    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    transaction.delete()

    return redirect("transaction_list")


# ==================================================
# CATEGORIES
# ==================================================
@login_required
def category_list(request):

    categories = Categorie.objects.filter(user=request.user)

    return render(request, "finance/categories.html", {
        "categories": categories
    })


@login_required
def add_category(request):

    if request.method == "POST":

        Categorie.objects.create(
            user=request.user,
            nom=request.POST.get("nom"),
            description=request.POST.get("description")
        )

        return redirect("category_list")

    return render(request, "finance/add_category.html")


@login_required
def edit_category(request, pk):

    category = get_object_or_404(Categorie, pk=pk, user=request.user)

    if request.method == "POST":
        category.nom = request.POST.get("nom")
        category.description = request.POST.get("description")
        category.save()
        return redirect("category_list")

    return render(request, "finance/edit_category.html", {
        "category": category
    })


@login_required
def delete_category(request, pk):

    category = get_object_or_404(Categorie, pk=pk, user=request.user)
    category.delete()

    return redirect("category_list")


# ==================================================
# BUDGETS
# ==================================================
@login_required
def budget_list(request):

    budgets = Budget.objects.filter(user=request.user)

    data = []

    for b in budgets:

        depense = Transaction.objects.filter(
            user=request.user,
            categorie=b.categorie
        ).aggregate(total=Sum("montant"))["total"] or 0

        budget = float(b.montant)
        depense = float(depense)

        reste = budget - depense

        data.append({
            "categorie": b.categorie.nom,
            "budget": budget,
            "depense": depense,
            "reste": reste
        })

    return render(request, "finance/budgets.html", {
        "data": data
    })


@login_required
def add_budget(request):

    categories = Categorie.objects.filter(user=request.user)

    if request.method == "POST":

        categorie_id = request.POST.get("categorie")
        montant = request.POST.get("montant")

        # ✅ AJOUT ICI
        mois = request.POST.get("mois")
        annee = request.POST.get("annee")

        Budget.objects.create(
            user=request.user,
            categorie_id=categorie_id,
            montant=montant,
            mois=mois,
            annee=annee
        )

        return redirect("budget_list")

    return render(request, "finance/add_budget.html", {
        "categories": categories
    })
@login_required
def edit_budget(request, pk):

    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    categories = Categorie.objects.filter(user=request.user)

    if request.method == "POST":
        budget.categorie_id = request.POST.get("categorie")
        budget.montant = request.POST.get("montant")
        budget.mois = request.POST.get("mois")
        budget.annee = request.POST.get("annee")
        budget.save()
        return redirect("budget_list")

    return render(request, "finance/edit_budget.html", {
        "budget": budget,
        "categories": categories
    })


@login_required
def delete_budget(request, pk):

    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    budget.delete()

    return redirect("budget_list")

@login_required
def budget_list(request):

    budgets = Budget.objects.filter(user=request.user)

    data = []

    for b in budgets:

        depense = Transaction.objects.filter(
            user=request.user,
            categorie=b.categorie
        ).aggregate(total=Sum("montant"))["total"] or 0

        reste = float(b.montant) - float(depense)

        pourcentage = (float(depense) / float(b.montant)) * 100 if b.montant else 0

        data.append({
            "id": b.id,
            "categorie": b.categorie,
            "montant": b.montant,
            "depense": depense,
            "reste": reste,
            "pourcentage": round(pourcentage, 1)
        })

    return render(request, "finance/budget_list.html", {
        "budgets": data
    })
# ==================================================
# PDF EXPORT
# ==================================================
@login_required
def export_pdf(request):

    revenus = Revenu.objects.filter(user=request.user).aggregate(
        total=Sum("montant")
    )["total"] or 0

    depenses = Transaction.objects.filter(user=request.user).aggregate(
        total=Sum("montant")
    )["total"] or 0

    solde = float(revenus) - float(depenses)

    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    p.drawString(100, 800, "RAPPORT FINANCIER")
    p.drawString(100, 770, f"Revenus: {revenus}")
    p.drawString(100, 750, f"Dépenses: {depenses}")
    p.drawString(100, 730, f"Solde: {solde}")

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="rapport.pdf"'

    return response
@login_required
def notification_list(request):

    notifications = Notification.objects.filter(
        user=request.user
    ).order_by("-date")

    return render(request, "finance/notifications.html", {
        "notifications": notifications
    })
@login_required
def mark_as_read(request, pk):

    notif = get_object_or_404(
        Notification,
        pk=pk,
        user=request.user
    )

    notif.lu = True
    notif.save()

    return redirect("notification_list")
def create_notification(user, titre, message):

    Notification.objects.create(
        user=user,
        titre=titre,
        message=message,
        lu=False
    )
@login_required
def historique(request):

    revenus = Revenu.objects.filter(user=request.user).values(
        "date", "source", "montant", "description"
    )

    depenses = Transaction.objects.filter(user=request.user).values(
        "date", "categorie__nom", "montant", "description"
    )

    historique = []

    # Revenus
    for r in revenus:
        historique.append({
            "date": r["date"],
            "type": "Revenu",
            "libelle": r["source"],
            "montant": r["montant"],
            "description": r["description"]
        })

    # Dépenses
    for d in depenses:
        historique.append({
            "date": d["date"],
            "type": "Dépense",
            "libelle": d["categorie__nom"],
            "montant": d["montant"],
            "description": d["description"]
        })

    # tri global
    historique = sorted(historique, key=lambda x: x["date"], reverse=True)

    return render(request, "finance/historique.html", {
        "historique": historique
    })
@login_required
def send_report(request):

    revenus = Revenu.objects.filter(user=request.user).aggregate(
        total=Sum("montant")
    )["total"] or 0

    depenses = Transaction.objects.filter(user=request.user).aggregate(
        total=Sum("montant")
    )["total"] or 0

    solde = float(revenus) - float(depenses)

    now = datetime.now().strftime("%d/%m/%Y %H:%M")

    message = f"""
RAPPORT FINANCIER

Date : {now}

Utilisateur : {request.user.email}

Revenus : {revenus} FBu
Dépenses : {depenses} FBu
Solde : {solde} FBu
"""

    send_mail(
        "Rapport financier",
        message,
        "misagos52@gmail.com",
        ["misagos52@gmail.com"],
        fail_silently=False,
    )

    return redirect("dashboard")