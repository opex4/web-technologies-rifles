from django.db import models
from django.db.models import ManyToManyField, ForeignKey


# Create your models here.
class Country(models.Model):
    name = models.TextField("Название страны", null=False)

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"

    def __str__(self):
        return self.name


class ArmedConflict(models.Model):
    title = models.TextField("Название конфликта", null=False)
    started_at = models.DateField("Дата начала", null=False)
    finished_at = models.DateField("Дата окончания", null=True, blank=True)

    class Meta:
        verbose_name = "Вооруженный конфликт"
        verbose_name_plural = "Вооруженные конфликты"

    def __str__(self):
        return self.title


class AmmoType(models.Model):
    title = models.TextField("Название калибра", null=False)

    class Meta:
        verbose_name = "Калибр"
        verbose_name_plural = "Калибры"

    def __str__(self):
        return self.title


class Constructor(models.Model):
    name = models.TextField("Имя конструктора", null=False)
    born_at = models.DateField("Дата рождения", null=False)
    died_at = models.DateField("Дата смерти", default=None, null=True, blank=True)

    class Meta:
        verbose_name = "Конструктор"
        verbose_name_plural = "Конструкторы"

    def __str__(self):
        return self.name


class TypeOfMount(models.Model):
    title = models.TextField("Тип крепления", null=False)
        
    class Meta:
        verbose_name = "Тип крепления"
        verbose_name_plural = "Типы крепления"

    def __str__(self):
        return self.title
    

class Rifle(models.Model):
    title = models.TextField("Название винтовки", null=False)
    description = models.TextField("Описание", null=False)
    created_at = models.DateField("Дата создания", null=False)
    constructors = ManyToManyField(Constructor, verbose_name="Создатели")
    country_of_origin = models.ForeignKey(Country, null=False, on_delete=models.CASCADE,
                                          verbose_name="Страна происхождения")
    ammo_type = ForeignKey(AmmoType, null=False, on_delete=models.CASCADE, verbose_name="Тип патрон")
    used_in_conflicts = ManyToManyField(ArmedConflict, verbose_name="Была использована в конфликтах", blank=True)
    types_of_mounts = ManyToManyField(TypeOfMount, verbose_name="Типы креплений", blank=True)
    picture = models.ImageField("Изображение", null=True, upload_to="rifles", blank=True)

    class Meta:
        verbose_name = "Винтовка"
        verbose_name_plural = "Винтовки"

    def __str__(self):
        return self.title
    
    
class Attachment(models.Model):
    title = models.TextField("Обвес", null=False)
    type_of_mount = ForeignKey(TypeOfMount, null=False, on_delete=models.CASCADE, verbose_name="Тип крепления")
        
    class Meta:
        verbose_name = "Обвес"
        verbose_name_plural = "Обвесы"

    def __str__(self):
        return self.title


class Loadout(models.Model):
    title = models.TextField("Название сборки", null=False)
    rifle = ForeignKey(Rifle, null=False, on_delete=models.CASCADE, verbose_name="Винтовка")
    creator = ForeignKey('general.UserProfile', null=False, on_delete=models.CASCADE, verbose_name="Создатель сборки")
    attachments = ManyToManyField(Attachment, verbose_name="Обвесы", blank=True)
    
    class Meta:
        verbose_name = "Сборка"
        verbose_name_plural = "Сборки"

    def __str__(self):
        return self.title