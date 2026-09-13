from django.contrib import admin

from rifles.models import Rifle, Constructor, AmmoType, Country, ArmedConflict, TypeOfMount, Attachment, Loadout, LoadoutAttachment


# Register your models here.
@admin.register(Rifle)
class RifleAdmin(admin.ModelAdmin):
    pass


@admin.register(Constructor)
class ConstructorAdmin(admin.ModelAdmin):
    pass


@admin.register(AmmoType)
class AmmoTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    pass


@admin.register(ArmedConflict)
class ArmedConflictAdmin(admin.ModelAdmin):
    pass

@admin.register(TypeOfMount)
class TypeOfMountAdmin(admin.ModelAdmin):
    pass

@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    pass

@admin.register(Loadout)
class LoadoutAdmin(admin.ModelAdmin):
    pass

@admin.register(LoadoutAttachment)
class LoadoutAttachmentAdmin(admin.ModelAdmin):
    pass