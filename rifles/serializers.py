from rest_framework import serializers

from rifles.models import Rifle, Constructor, AmmoType, ArmedConflict, Country, TypeOfMount, Attachment, Loadout


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class ArmedConflictSerializer(serializers.ModelSerializer):
    countries = CountrySerializer(many=True, read_only=True)

    class Meta:
        model = ArmedConflict
        fields = '__all__'


class AmmoTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmmoType
        fields = '__all__'


class ConstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Constructor
        fields = '__all__'


class RifleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rifle
        fields = '__all__'
        
        
class TypeOfMountSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeOfMount
        fields = '__all__'
        
        
class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = '__all__'
        
        
class LoadoutSerializer(serializers.ModelSerializer):
    creator = serializers.CharField(source='creator.user.username', read_only=True)
    class Meta:
        model = Loadout
        exclude = ['id']
