from rest_framework import viewsets, mixins

from rifles.models import Rifle, AmmoType, Country, ArmedConflict, Constructor, TypeOfMount, Attachment, Loadout
from rifles.serializers import RifleSerializer, AmmoTypeSerializer, CountrySerializer, ArmedConflictSerializer, \
    ConstructorSerializer, TypeOfMountSerializer, AttachmentSerializer, LoadoutSerializer

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
    
    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     qs = qs.filter(user=self.request.user)
