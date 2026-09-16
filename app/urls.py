"""
URL configuration for app project.

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
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

from general.api import UserProfileViewSet
import rifles.views
from rifles.api import RiflesViewSet, AmmoTypesViewSet, ConstructorsViewSet, CountriesViewSet, ArmedConflictsViewSet, \
    TypeOfMountViewSet, AttachmentViewSet, LoadoutViewSet

router = DefaultRouter()
router.register('rifles', RiflesViewSet, basename='rifles')
router.register('ammo_types', AmmoTypesViewSet, basename='ammo_types')
router.register('constructors', ConstructorsViewSet, basename='constructors')
router.register('countries', CountriesViewSet, basename='countries')
router.register('armed_conflicts', ArmedConflictsViewSet, basename='armed_conflicts')
router.register('types_of_mounts', TypeOfMountViewSet, basename='types_of_mounts')
router.register('attachments', AttachmentViewSet, basename='attachments')
router.register('loadouts', LoadoutViewSet, basename='loadouts')
router.register('users', UserProfileViewSet, basename='users')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', rifles.views.ShowRiflesView.as_view(), name='show-rifles'),
    path('api/', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
