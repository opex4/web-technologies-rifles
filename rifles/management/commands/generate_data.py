from django.core.management.base import BaseCommand

from faker import Faker

from rifles.models import Country, ArmedConflict, AmmoType, Constructor, TypeOfMount, Rifle, Attachment, Loadout
from general.models import UserProfile
from django.contrib.auth.models import User
import datetime

class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker(['ru_RU'])
        
        countries = [Country.objects.create(name=fake.country()) for _ in range(296)]
        ammo_types = [AmmoType.objects.create(title=fake.word()) for _ in range(1000)]
        constructors = []
        for _ in range(1000):
            born_at = fake.date_between(start_date=datetime.date(1900, 1, 1), end_date=datetime.date(1940, 1, 1))
            died_at = fake.date_between(start_date=datetime.date(1980, 1, 1), end_date=datetime.date(1990, 1, 1)) if fake.boolean(chance_of_getting_true=70) else None
            constructors.append(Constructor.objects.create(
                name=fake.name(),
                born_at=born_at,
                died_at=died_at
            ))
        conflicts = []
        for _ in range(1000):
            started_at = fake.date_between(start_date=datetime.date(2000, 1, 1), end_date=datetime.date(2010, 1, 1))
            finished_at = fake.date_between(start_date=started_at, end_date=datetime.date(2020, 1, 1)) if fake.boolean(chance_of_getting_true=80) else None
            conflicts.append(ArmedConflict.objects.create(
                title=fake.sentence(nb_words=3).rstrip('.'),
                started_at=started_at,
                finished_at=finished_at
            ))
        mounts = [TypeOfMount.objects.create(title=fake.unique.word()) for _ in range(250)]

        rifles = []
        for _ in range(1000):
            rifle = Rifle.objects.create(
                title=fake.sentence(nb_words=2).rstrip('.'),
                description=fake.text(max_nb_chars=200),
                created_at=fake.date_between(start_date=datetime.date(1960, 1, 1), end_date=datetime.date(1990, 1, 1)),
                country_of_origin=fake.random_element(countries),
                ammo_type=fake.random_element(ammo_types),
            )
            rifle.constructors.add(*fake.random_elements(constructors, length=2, unique=True))
            rifle.used_in_conflicts.add(*fake.random_elements(conflicts, length=2, unique=True))
            rifle.types_of_mounts.add(*fake.random_elements(mounts, length=2, unique=True))
            rifles.append(rifle)

        for _ in range(1000):
            Attachment.objects.create(
                title=fake.word(),
                type_of_mount=fake.random_element(mounts),
            )
            
        user, _ = User.objects.get_or_create(username='test_user')
        user.set_password('test') 
        user.save()        
        profile, _ = UserProfile.objects.get_or_create(user=user, defaults={'type': 'builder'})
        
        loadouts = []
        for _ in range(1000):
            rifle = fake.random_element(rifles)
            loadout = Loadout.objects.create(
                title=fake.sentence(nb_words=2).rstrip('.'),
                rifle=rifle,
                creator=profile,
            )
            
            allowed_mounts = list(rifle.types_of_mounts.all())
            if allowed_mounts:
                chosen_mount = fake.random_element(allowed_mounts)
                compatible = [a for a in Attachment.objects.filter(type_of_mount=chosen_mount)]
                if compatible:
                    loadout.attachments.add(fake.random_element(compatible))
            loadouts.append(loadout)
