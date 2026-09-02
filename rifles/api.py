from rest_framework import viewsets, mixins
from general.models import UserProfile
from general.permissions import BasePermission, ReaderPermissions, BuilderPermissions, ModeratorPermissions, \
    CreatorLoadoutPermissions

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
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [ReaderPermissions()]
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [ModeratorPermissions()]
        return [BasePermission()]

class AmmoTypesViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin, 
    viewsets.GenericViewSet
):
    queryset = AmmoType.objects.all()
    serializer_class = AmmoTypeSerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [ReaderPermissions()]
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [ModeratorPermissions()]
        return [BasePermission()]

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
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [ReaderPermissions()]
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [ModeratorPermissions()]
        return [BasePermission()]

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
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [ReaderPermissions()]
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [ModeratorPermissions()]
        return [BasePermission()]

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
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [ReaderPermissions()]
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [ModeratorPermissions()]
        return [BasePermission()]
    
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
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [ReaderPermissions()]
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [ModeratorPermissions()]
        return [BasePermission()]

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
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [BuilderPermissions()]
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [ModeratorPermissions()]
        return [BasePermission()]
    
class LoadoutViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = LoadoutSerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [BuilderPermissions()]
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [BuilderPermissions(), CreatorLoadoutPermissions()]
        return [BasePermission()]
    
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user.userprofile)
        
    def get_queryset(self):
        user = self.request.user
        if user.userprofile.type in [UserProfile.Type.builder]:
            return Loadout.objects.filter(creator=user.userprofile)
        if user.userprofile.type in [UserProfile.Type.moderator]:
            return Loadout.objects.all()
        return Loadout.objects.none()
    
    # @action(detail=False, url_path="create-loadout", methods=['POST'])
    # def create_loadout(self, request, *args, **kwargs):
        
    #     return super().create(request, *args, **kwargs)
    
    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     qs = qs.filter(user=self.request.user)
