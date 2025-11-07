from rest_framework import serializers

from rifles.models import Rifle, Constructor, AmmoType, ArmedConflict, Country


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
    # constructors = ConstructorSerializer(many=True, read_only=True)
    # used_in_conflicts = ArmedConflictSerializer(many=True, read_only=True)
    # country_of_origin = CountrySerializer(read_only=True)
    # ammo_type = AmmoTypeSerializer(read_only=True)


    class Meta:
        model = Rifle
        fields = '__all__'
