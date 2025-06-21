"""
URL configuration for the *edplatform* project.

–  “Site” pages (HTML templates) are declared FIRST so they win the
   URL-resolver race against similarly-named API routes.
–  API endpoints live under /api/auth/ and come afterwards.
"""

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    # ──────────────────────────────────────────
    # 1)  Public / session-based HTML pages
    # ──────────────────────────────────────────
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="login"),
        name="logout",
    ),
    path(
        "signup/",
        TemplateView.as_view(template_name="signup.html"),
        name="signup",
    ),
    path(
        "home/",
        TemplateView.as_view(template_name="home.html"),
        name="home",
    ),
    path(
        "dashboard/",
        TemplateView.as_view(template_name="dashboard.html"),
        name="dashboard",
    ),
    # Root URL → login page (feel free to change)
    path(
        "",
        auth_views.LoginView.as_view(template_name="login.html"),
        name="root",
    ),

    # ──────────────────────────────────────────
    # 2)  Feature-app URLConfs
    # ──────────────────────────────────────────
    path("problems/", include("problems.urls")),
    path("blogs/",    include("blogs.urls")),

    # ──────────────────────────────────────────
    # 3)  API  (dj-rest-auth / DRF)
    #     Kept AFTER site pages so names don't clash
    # ──────────────────────────────────────────
    path("api/auth/",              include("dj_rest_auth.urls")),
    path("api/auth/registration/", include("dj_rest_auth.registration.urls")),
    # path("api/auth/jwt/",       include("dj_rest_auth.jwt.urls")),  # ← enable if/when you use JWT

    # ──────────────────────────────────────────
    # 4)  Django Admin
    # ──────────────────────────────────────────
    path("admin/", admin.site.urls),
]
