"""quizapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from ninja import NinjaAPI
from ninja.security import django_auth
from .api import api
# api = NinjaAPI(auth=django_auth, csrf=True)
# ... the rest of your URLconf goes here ...

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/",api.urls),
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)