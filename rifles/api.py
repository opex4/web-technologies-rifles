from rest_framework import viewsets, mixins
from general.models import UserProfile
from general.permissions import BasePermission, ReaderPermissions, BuilderPermissions, ModeratorPermissions, \
    CreatorLoadoutPermissions
    
from django.db.models import Avg, Count, Max, Min
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers

from openpyxl import Workbook
from django.http import FileResponse
from io import BytesIO

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
    
    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()
    
    @action(url_path="stats", methods=["GET"], detail=False, permission_classes=[ModeratorPermissions])
    def get_stats(self, request, *args, **kwargs):
        stats = Rifle.objects.aggregate(
            count=Count("*"),
            avg=Avg("id"),
            max=Max("id"),
            min=Min("id")
        )
        serializer = self.StatsSerializer(instance=stats)
        return Response(serializer.data)
    
    @action(url_path="excel", methods=["GET"], detail=False, permission_classes=[ModeratorPermissions])
    def get_excel(self, request, *args, **kwargs):
        wb = Workbook()
        ws = wb.active
        ws.title = "Винтовки"
        
        headers = ['ID', 'Название', 'Описание', 'Дата создания', 'Патрон', 'Страна']
        ws.append(headers)
        
        for rifle in self.get_queryset():
            ws.append([
                rifle.id,
                rifle.title,
                rifle.description,
                rifle.created_at,
                rifle.ammo_type.title,
                rifle.country_of_origin.name,
            ])
            
        output = BytesIO()
        wb.save(output)
        output.seek(0)
        
        return FileResponse(
            output,
            as_attachment=True,
            filename='rifles.xlsx',
        )


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
    
    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()
    
    @action(url_path="stats", methods=["GET"], detail=False, permission_classes=[ModeratorPermissions])
    def get_stats(self, request, *args, **kwargs):
        stats = AmmoType.objects.aggregate(
            count=Count("*"),
            avg=Avg("id"),
            max=Max("id"),
            min=Min("id")
        )
        serializer = self.StatsSerializer(instance=stats)
        return Response(serializer.data)


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
    
    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()
    
    @action(url_path="stats", methods=["GET"], detail=False, permission_classes=[ModeratorPermissions])
    def get_stats(self, request, *args, **kwargs):
        stats = Country.objects.aggregate(
            count=Count("*"),
            avg=Avg("id"),
            max=Max("id"),
            min=Min("id")
        )
        serializer = self.StatsSerializer(instance=stats)
        return Response(serializer.data)


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
    
    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()
    
    @action(url_path="stats", methods=["GET"], detail=False, permission_classes=[ModeratorPermissions])
    def get_stats(self, request, *args, **kwargs):
        stats = ArmedConflict.objects.aggregate(
            count=Count("*"),
            avg=Avg("id"),
            max=Max("id"),
            min=Min("id")
        )
        serializer = self.StatsSerializer(instance=stats)
        return Response(serializer.data)


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
    
    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()
    
    @action(url_path="stats", methods=["GET"], detail=False, permission_classes=[ModeratorPermissions])
    def get_stats(self, request, *args, **kwargs):
        stats = Constructor.objects.aggregate(
            count=Count("*"),
            avg=Avg("id"),
            max=Max("id"),
            min=Min("id")
        )
        serializer = self.StatsSerializer(instance=stats)
        return Response(serializer.data)
    
    
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
    
    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()
    
    @action(url_path="stats", methods=["GET"], detail=False, permission_classes=[ModeratorPermissions])
    def get_stats(self, request, *args, **kwargs):
        stats = TypeOfMount.objects.aggregate(
            count=Count("*"),
            avg=Avg("id"),
            max=Max("id"),
            min=Min("id")
        )
        serializer = self.StatsSerializer(instance=stats)
        return Response(serializer.data)


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
    
    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()
    
    @action(url_path="stats", methods=["GET"], detail=False, permission_classes=[ModeratorPermissions])
    def get_stats(self, request, *args, **kwargs):
        stats = Attachment.objects.aggregate(
            count=Count("*"),
            avg=Avg("id"),
            max=Max("id"),
            min=Min("id")
        )
        serializer = self.StatsSerializer(instance=stats)
        return Response(serializer.data)
    
    
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
    
    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()
    
    @action(url_path="stats", methods=["GET"], detail=False, permission_classes=[ModeratorPermissions])
    def get_stats(self, request, *args, **kwargs):
        stats = Loadout.objects.aggregate(
            count=Count("*"),
            avg=Avg("id"),
            max=Max("id"),
            min=Min("id")
        )
        serializer = self.StatsSerializer(instance=stats)
        return Response(serializer.data)
    
