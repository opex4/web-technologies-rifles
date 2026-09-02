from rest_framework.permissions import BasePermission
from general.models import UserProfile

class ModeratorPermissions(BasePermission):
    message = "Нужен доступ модератора"
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.userprofile.type == UserProfile.Type.moderator
    
class BuilderPermissions(BasePermission):
    message = "Нужен доступ сборщика"
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.userprofile.type in [
            UserProfile.Type.builder,
            UserProfile.Type.moderator,
        ]
    
class ReaderPermissions(BasePermission):
    message = "Нужен доступ читателя"
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.userprofile.type in [
            UserProfile.Type.reader,
            UserProfile.Type.builder,
            UserProfile.Type.moderator,
        ]
        
class CreatorLoadoutPermissions(BasePermission):
    message = "Нужен доступ создателя сборки"
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        return request.user.userprofile == obj.creator
    
class SecondFactorPermission(BasePermission):
    message = "Нужен второй фактор доступа"
    def has_object_permission(self, request, view, obj):
        return request.session.get('second') == True