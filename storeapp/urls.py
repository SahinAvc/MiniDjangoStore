from django.urls import path
from . import views

app_name = "storeapp"

urlpatterns = [
    # Herkese açık vitrin
    path("", views.home, name="home"),
    path("ilan/<int:pk>/", views.product_detail, name="product_detail"),

    # Üyelik
    path("giris/", views.login_view, name="login"),
    path("kayit/", views.register_view, name="register"),
    path("cikis/", views.logout_view, name="logout"),

    # Satıcı paneli (giriş gerekli)
    path("panel/", views.panel_dashboard, name="panel_dashboard"),
    path("panel/ilan-ver/", views.panel_product_create, name="panel_product_create"),
    path("panel/ilan/<int:pk>/duzenle/", views.panel_product_update, name="panel_product_update"),
    path("panel/ilan/<int:pk>/sil/", views.panel_product_delete, name="panel_product_delete"),
]
