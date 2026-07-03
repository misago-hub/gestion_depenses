from django.urls import path
from . import views

urlpatterns = [

    # TRANSACTIONS
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/add/', views.add_transaction, name='add_transaction'),
    
    # CATEGORIES
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('categories/delete/<int:pk>/', views.delete_category, name='delete_category'),

    # BUDGETS
    path('budgets/', views.budget_list, name='budget_list'),
    path('budgets/add/', views.add_budget, name='add_budget'),
    path('budgets/edit/<int:pk>/', views.edit_budget, name='edit_budget'),
    path('budgets/delete/<int:pk>/', views.delete_budget, name='delete_budget'),

    # EXPORT PDF
    path('export/pdf/', views.export_pdf, name='export_pdf'),
    # REVENUS
    path("revenus/", views.revenu_list, name="revenu_list"),
    path("revenus/add/", views.add_revenu, name="add_revenu"),
    path("revenus/delete/<int:pk>/", views.delete_revenu, name="delete_revenu"),
    # NOTIFICATIONS
    path("notifications/", views.notification_list, name="notification_list"),
    path("notifications/read/<int:pk>/", views.mark_as_read, name="mark_as_read"),
    # HISTORIQUES
    path("historique/", views.historique, name="historique"),
    # RAPPORTS
    path("report/send/", views.send_report, name="send_report"),
  ]