"""
URL configuration for edplatform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),                   # classic session-based admin
    path("api/auth/",             include("dj_rest_auth.urls")),            # login/logout
    path("api/auth/registration/",include("dj_rest_auth.registration.urls")),# sign-up flow
    # path("api/auth/jwt/",         include("dj_rest_auth.jwt.urls")),        # obtain/refresh
    path('',      TemplateView.as_view(template_name='login.html'), name='login-page'),
    path('home/', TemplateView.as_view(template_name='home.html'),  name='home-page'),
    path("signup/", TemplateView.as_view(template_name="signup.html"), name="signup"),
    path("login/", TemplateView.as_view(template_name="login.html"), name="login"),
    path("dashboard/", TemplateView.as_view(template_name="dashboard.html"), name="dashboard"),
]

