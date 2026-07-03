from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required

from .models import User
# =========================
# LOGIN
# =========================
def login_view(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:

            if user.statut != "autorisé":
                return render(request, "auth/login.html", {
                    "error": "Compte en attente de validation"
                })

            auth_login(request, user)
            return redirect("dashboard")

        return render(request, "auth/login.html", {
            "error": "Email ou mot de passe incorrect"
        })

    return render(request, "auth/login.html")

# =========================
# REGISTER
# =========================
def register_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            return render(request, "auth/register.html", {
                "error": "Les mots de passe ne correspondent pas"
            })

        if User.objects.filter(email=email).exists():
            return render(request, "auth/register.html", {
                "error": "Cet email existe déjà"
            })

        User.objects.create(
            nom=username,
            email=email,
            password=make_password(password1),
            role="utilisateur",
            statut="en attente"
        )

        return redirect("login")

    return render(request, "auth/register.html")


# =========================
# LOGOUT
# =========================
def logout_view(request):
    logout(request)
    return redirect("login")


# =========================
# ADMIN USERS
# =========================
@login_required
def admin_users_view(request):

    if request.user.role != "admin":
        return redirect('dashboard')

    users = User.objects.all().order_by('-id')

    return render(request, "auth/admin_users.html", {
        "users": users
    })

# =========================
# APPROVE USER
# =========================
def approve_user(request, user_id):

    user = get_object_or_404(User, id=user_id)
    user.statut = "autorisé"
    user.save()

    return redirect('admin_users')


# =========================
# SUSPEND USER
# =========================
def suspend_user(request, user_id):

    user = get_object_or_404(User, id=user_id)
    user.statut = "en attente"
    user.save()

    return redirect('admin_users')


# =========================
# LOGIN AS USER
# =========================
def login_as_user(request, user_id):

    user = get_object_or_404(User, id=user_id)

    request.session['admin_id'] = request.user.id
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)

    return redirect('dashboard')


# =========================
# RETOUR ADMIN
# =========================
def retour_admin(request):

    admin_id = request.session.get('admin_id')

    if admin_id:
        admin = User.objects.get(id=admin_id)
        admin.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, admin)
        del request.session['admin_id']

    return redirect('dashboard')