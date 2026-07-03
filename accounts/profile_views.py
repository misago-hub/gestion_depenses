from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

# ==========================
# MON PROFIL
# ==========================
@login_required
def profile(request):

    return render(request, "auth/profile.html")


# ==========================
# MODIFIER LE PROFIL
# ==========================
@login_required
def edit_profile(request):

    user = request.user

    if request.method == "POST":

        user.nom = request.POST.get("nom")
        user.email = request.POST.get("email")

        if request.FILES.get("photo"):
            user.photo = request.FILES["photo"]

        user.save()

        return redirect("profile")

    return render(request, "auth/edit_profile.html")
@login_required
def change_password(request):

    if request.method == "POST":

        ancien = request.POST.get("ancien")
        nouveau = request.POST.get("nouveau")
        confirmer = request.POST.get("confirmer")

        if not request.user.check_password(ancien):
            messages.error(request, "Ancien mot de passe incorrect.")
            return redirect("change_password")

        if nouveau != confirmer:
            messages.error(request, "Les deux mots de passe ne correspondent pas.")
            return redirect("change_password")

        request.user.set_password(nouveau)
        request.user.save()

        update_session_auth_hash(request, request.user)

        messages.success(request, "Mot de passe modifié avec succès.")

        return redirect("profile")

    return render(request, "auth/change_password.html")