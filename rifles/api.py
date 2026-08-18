from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt 

from rifles.models import Rifle, AmmoType, Country, ArmedConflict, Constructor, TypeOfMount, Attachment, Loadout
from rifles.serializers import RifleSerializer, AmmoTypeSerializer, CountrySerializer, ArmedConflictSerializer, \
    ConstructorSerializer, TypeOfMountSerializer, AttachmentSerializer, LoadoutSerializer

@method_decorator(csrf_exempt, name='dispatch')
class RiflesViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Rifle.objects.all()
    serializer_class = RifleSerializer
    permission_classes = [AllowAny]

@method_decorator(csrf_exempt, name='dispatch')
class AmmoTypesViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    queryset = AmmoType.objects.all()
    serializer_class = AmmoTypeSerializer
    permission_classes = [AllowAny]

@method_decorator(csrf_exempt, name='dispatch')
class CountriesViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [AllowAny]

@method_decorator(csrf_exempt, name='dispatch')
class ArmedConflictsViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = ArmedConflict.objects.all()
    serializer_class = ArmedConflictSerializer
    permission_classes = [AllowAny]

@method_decorator(csrf_exempt, name='dispatch')
class ConstructorsViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Constructor.objects.all()
    serializer_class = ConstructorSerializer
    permission_classes = [AllowAny]
    
@method_decorator(csrf_exempt, name='dispatch')
class TypeOfMountViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = TypeOfMount.objects.all()
    serializer_class = TypeOfMountSerializer
    permission_classes = [AllowAny]

@method_decorator(csrf_exempt, name='dispatch')
class AttachmentViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    permission_classes = [AllowAny]
    
@method_decorator(csrf_exempt, name='dispatch')
class LoadoutViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Loadout.objects.all()
    serializer_class = LoadoutSerializer
    permission_classes = [AllowAny]

