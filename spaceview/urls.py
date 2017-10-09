"""spaceview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.contrib import admin
from django.conf.urls import url, include
from app import views
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'movements', views.MovementViewSet, base_name = "movement")
router.register(r'sensors', views.SensorViewSet, base_name = "sensor")

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^api', include(router.urls)),
    url(r'^dashboard', views.DashboardView.as_view()),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns += [
    url(r'^admin/', admin.site.urls)
]
