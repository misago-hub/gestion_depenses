from django.urls import path
from . import views
from . import admin_views

urlpatterns = [

    # Dashboard utilisateur
    path("", views.dashboard, name="dashboard"),

    # Dashboard administrateur
    path("admin/", views.admin_dashboard, name="admin_dashboard"),

    # ============================
    # GESTION DES UTILISATEURS
    # ============================

    path(
        "users/",
        admin_views.users_list,
        name="users_list"
    ),

    path(
        "users/autoriser/<int:pk>/",
        admin_views.autoriser_user,
        name="autoriser_user"
    ),

    path(
        "users/suspendre/<int:pk>/",
        admin_views.suspendre_user,
        name="suspendre_user"
    ),

    path(
        "users/supprimer/<int:pk>/",
        admin_views.supprimer_user,
        name="supprimer_user"
    ),

]