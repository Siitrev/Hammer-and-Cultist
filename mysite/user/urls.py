from . import views
from django.urls import path, re_path

urlpatterns = [
    path("register/", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name="logout"),
    re_path(r'activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,40})/',  
        views.activate, name='activate'),
    path("reset-password/", views.password_reset_request, name="reset-password"),
    path("reset-password/<str:uidb64>/<str:token>/", views.password_reset_change, name="reset-password-change")
]
