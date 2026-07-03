from django.contrib import admin
from django.urls import path, include

# AJOUTER CES 2 LIGNES
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path("admin/", admin.site.urls),

    path("auth/", include("accounts.urls")),

    path("finance/", include("finance.urls")),

    path("", include("dashboard.urls")),

]

# AJOUTER CES LIGNES A LA FIN
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)