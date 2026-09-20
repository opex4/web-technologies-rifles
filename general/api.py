from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import pyotp

class UserProfileViewSet(GenericViewSet):    
    @action(url_path="my", methods=["GET"], detail=False)
    def get_my(self, *args, **kwargs):
        date = {
            'username': self.request.user.username if self.request.user.is_authenticated else '',
            'isAuth': self.request.user.is_authenticated,
            'isStaff': self.request.user.is_staff,
        }
        if self.request.user.is_authenticated:
            date.update({
                'type': self.request.user.userprofile.type,
                'second': self.request.session.get('second') or False,
            })
        return Response(date)
    
    @action(url_path="list", methods=["GET"], detail=False)
    def get_list(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.userprofile.type != 'moderator':
            return Response({"status": "failed"}, status=403)
        else:
            usernames = User.objects.values_list('username', flat=True)
            return Response([{'username': name} for name in usernames])
    
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
             
    @action(url_path="create", methods=["POST"], detail=False)
    def process_create_user(self, *args, **kwargs):
        class CreateUserSerialiser(serializers.Serializer):
            username = serializers.CharField()
            password = serializers.CharField()
            
        serializer = CreateUserSerialiser(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        if User.objects.filter(username=username).exists():
            return Response({
                "status": "usernameFailed"
            }, status=400)
        
        user = User.objects.create_user(username=username, password=password) 
            
        login(self.request, user)
        return Response({
            "status": "success"
        })

    @action(url_path="second-login", methods=["Post"], detail=False)
    def second_login(self, *args, **kwargs):
        key = self.request.user.userprofile.totp_key
        t = pyotp.totp.TOTP(key)
        key = self.request.data.get('key')
        if key == t.now():
            self.request.session['second'] = True  
            return Response({
                "status": "success"
            })
        return Response({
            "status": "failed"
        })

    @action(url_path="get-totp", methods=["GET"], detail=False)
    def get_totp(self, *args, **kwargs):
        self.request.user.userprofile.totp_key = pyotp.random_base32()
        self.request.user.userprofile.save()
        
        url =  pyotp.totp.TOTP(self.request.user.userprofile.totp_key).provisioning_uri(
            name=self.request.user.username, issuer_name="Rifles"
        )
        
        return Response ({
            "url": url
        })
