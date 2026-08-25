from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth import authenticate, login, logout

class UserProfileViewSet(GenericViewSet):    
    @action(url_path="my", methods=["GET"], detail=False)
    def get_my(self, *args, **kwargs):
        return Response({
            'username': self.request.user.username if self.request.user.is_authenticated else '',
            'isAuth': self.request.user.is_authenticated,
            'isStaff': self.request.user.is_staff,
        })
    
    @action(url_path="login", methods=["POST"], detail=False)
    def process_login(self, *args, **kwargs):
        class LoginSerialiser(serializers.Serializer):
            username = serializers.CharField()
            password = serializers.CharField()
            
        serializer = LoginSerialiser(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = authenticate(username=username, password=password)
        if user:
            login(self.request, user)
        else:
            return Response({
                "status": "failed"
            }, status=401)
        
        return Response({
            "status": "success"
        })
        
    @action(url_path="logout", methods=["POST"], detail=False)
    def process_logout(self, *args, **kwargs):
        logout(self.request)
        
        return Response ({
            "status": "success"
        })