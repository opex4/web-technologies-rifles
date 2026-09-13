from rest_framework import serializers

from rifles.models import Rifle, Constructor, AmmoType, ArmedConflict, Country, TypeOfMount, Attachment, Loadout, LoadoutAttachment


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
    attachments = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Attachment.objects.all(),
        required=False
    )
    
    class Meta:
        model = Loadout
        fields = '__all__'
        
    def validate(self, data):
        rifle = data.get('rifle') or getattr(self.instance, 'rifle', None)
        
        if 'attachments' in data:
                attachments = data['attachments']
        elif self.instance:
            attachments = list(self.instance.attachments.all())
        else:
            attachments = []
        
        if rifle and attachments:
            allowed_mounts = set(rifle.types_of_mounts.values_list('id', flat=True))
            used_mounts = set()
            
            for attachment in attachments:
                if attachment.type_of_mount_id not in allowed_mounts:
                    raise serializers.ValidationError("Обвес несовместим с винтовкой")
                
                if attachment.type_of_mount_id in used_mounts:
                    raise serializers.ValidationError("Нельзя добавить два обвеса с одним типом крепления")
                used_mounts.add(attachment.type_of_mount_id)
        
        return data
    
    def create(self, validated_data):
        attachments_data = validated_data.pop('attachments', [])
        loadout = Loadout.objects.create(**validated_data)
        
        for attachment in attachments_data:
            LoadoutAttachment.objects.create(
                loadout=loadout,
                attachment=attachment
            )
        
        return loadout
    
    def update(self, instance, validated_data):
        attachments_data = validated_data.pop('attachments', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if attachments_data is not None:
            instance.attachments.clear()
            for attachment in attachments_data:
                LoadoutAttachment.objects.create(
                    loadout=instance,
                    attachment=attachment
                )
        
        return instance
