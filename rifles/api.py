from rest_framework import viewsets, mixins

from rifles.models import Rifle, AmmoType, Country, ArmedConflict, Constructor
from rifles.serializers import RifleSerializer, AmmoTypeSerializer, CountrySerializer, ArmedConflictSerializer, \
    ConstructorSerializer


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


class AmmoTypesViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    queryset = AmmoType.objects.all()
    serializer_class = AmmoTypeSerializer


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
