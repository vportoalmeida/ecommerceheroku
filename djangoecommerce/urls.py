"""djangoecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from core.views import index, contact, register
from django.contrib.auth.views import login, logout

urlpatterns = [
    # ------------------------------------------ Base Routes -----------------------------------------------------------
    url(r'^$', index, name='index'),
    url(r'^contato/$', contact, name='contact'),
    url(r'^catalogo/', include('catalog.urls', namespace='catalog')),
    # -------------------------------------- Authentication Related ----------------------------------------------------
    url(r'^entrar/$', login, {'template_name': 'login.html'}, name='login'),
    url(r'^sair/$', logout, {'next_page': 'index'}, name='logout'),
    # ------------------------------------------- Register -------------------------------------------------------------
    url(r'^registro/$', register, name='register'),
    # ---------------------------------------- Django Admin Routes -----------------------------------------------------
    url(r'^admin/', admin.site.urls),
]
