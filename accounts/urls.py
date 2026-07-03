from django.urls import path
from . import views
from . import profile_views
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    path('admin/users/', views.admin_users_view, name='admin_users'),
    path('approve/<int:user_id>/', views.approve_user, name='approve_user'),
    path('suspend/<int:user_id>/', views.suspend_user, name='suspend_user'),

    path('login-as/<int:user_id>/', views.login_as_user, name='login_as_user'),
    path('retour-admin/', views.retour_admin, name='retour_admin'),
    path("profile/", profile_views.profile, name="profile"),
    path("profile/edit/", profile_views.edit_profile, name="edit_profile"),
    path(
    "profile/password/",
    profile_views.change_password,
    name="change_password"
),
]