from django.test import TestCase
from model_bakery import baker
from rest_framework.test import APIClient
from general.models import UserProfile
from django.contrib.auth.models import User

from rifles.models import Country, AmmoType, Constructor, ArmedConflict, Rifle, TypeOfMount, Attachment, Loadout


# Create your tests here.
class RiflesTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        country = baker.make(Country)
        ammo_type = baker.make(AmmoType)
        constructor = baker.make(Constructor)
        armed_conflict = baker.make(ArmedConflict)
        rifle = baker.make(
            Rifle,
            ammo_type=ammo_type,
            constructors=[constructor],
            used_in_conflicts=[armed_conflict],
            country_of_origin=country,
        )

        req = self.client.get('/api/rifles/')
        data = req.json()

        assert data[0]['title'] == rifle.title
        assert data[0]['description'] == rifle.description
        assert data[0]['created_at'] == rifle.created_at.isoformat()
        assert data[0]['constructors'][0] == constructor.id
        assert data[0]['ammo_type'] == ammo_type.id
        assert data[0]['used_in_conflicts'][0] == armed_conflict.id

    def test_post(self):
        country = baker.make(Country)
        ammo_type = baker.make(AmmoType)
        constructor = baker.make(Constructor)
        armed_conflict = baker.make(ArmedConflict)
        rifle = {
            "title": 'Rifle',
            'description': 'Rifle description',
            'created_at': '2025-10-27',
            "constructors": [constructor.id],
            "ammo_type": ammo_type.id,
            "country_of_origin": country.id,
            "used_in_conflicts": [armed_conflict.id],
        }

        req = self.client.post('/api/rifles/', rifle)
        data = req.json()

        assert data['title'] == rifle['title']
        assert data['description'] == rifle['description']
        assert data['created_at'] == rifle['created_at']
        assert data['constructors'][0] == constructor.id
        assert data['ammo_type'] == ammo_type.id
        assert data['used_in_conflicts'][0] == armed_conflict.id

    def test_delete(self):
        rifles = baker.make(Rifle, 10)

        req = self.client.get('/api/rifles/')
        assert len(req.json()) == 10

        self.client.delete(f'/api/rifles/{rifles[3].id}/')
        req2 = self.client.get('/api/rifles/')
        assert len(req2.json()) == 9

    def test_update(self):
        country = baker.make(Country)
        ammo_type = baker.make(AmmoType)
        constructor = baker.make(Constructor)
        armed_conflict = baker.make(ArmedConflict)
        rifle = baker.make(
            Rifle,
            ammo_type=ammo_type,
            constructors=[constructor],
            used_in_conflicts=[armed_conflict],
            country_of_origin=country,
        )
        k12 = 'Калак-12, с затворная задержка как у М16'
        rifle.refresh_from_db()
        req = self.client.put(f'/api/rifles/{rifle.id}/', {
            'title': k12,
            'description': rifle.description,
            'created_at': rifle.created_at.isoformat(),
            'country_of_origin': country.id,
            'ammo_type': ammo_type.id,
            'used_in_conflicts': [armed_conflict.id],
            'constructors': [constructor.id],
        })
        assert req.status_code == 200

        req = self.client.get(f'/api/rifles/{rifle.id}/')
        assert req.json()['title'] == k12


class CountriesTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        country = baker.make(Country, name='Russia')

        req = self.client.get('/api/countries/')
        data = req.json()

        assert data[0]['name'] == country.name
        assert data[0]['id'] == country.id

    def test_post(self):
        country_data = {
            "name": "United States"
        }

        req = self.client.post('/api/countries/', country_data)
        data = req.json()

        assert data['name'] == country_data['name']
        assert 'id' in data

    def test_delete(self):
        countries = baker.make(Country, 5)

        req = self.client.get('/api/countries/')
        assert len(req.json()) == 5

        self.client.delete(f'/api/countries/{countries[2].id}/')
        req2 = self.client.get('/api/countries/')
        assert len(req2.json()) == 4

    def test_update(self):
        country = baker.make(Country, name='Germany')

        new_name = 'Federal Republic of Germany'
        req = self.client.put(f'/api/countries/{country.id}/', {
            'name': new_name,
        })
        assert req.status_code == 200

        req = self.client.get(f'/api/countries/{country.id}/')
        assert req.json()['name'] == new_name


class ArmedConflictsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        conflict = baker.make(ArmedConflict)

        req = self.client.get('/api/armed_conflicts/')
        data = req.json()

        assert data[0]['title'] == conflict.title
        assert data[0]['started_at'] == conflict.started_at.isoformat()

    def test_post(self):
        conflict_data = {
            "title": "World War II",
            "started_at": "1939-09-01",
            "finished_at": "1945-09-02"
        }

        req = self.client.post('/api/armed_conflicts/', conflict_data)
        data = req.json()

        assert data['title'] == conflict_data['title']
        assert data['started_at'] == conflict_data['started_at']
        assert data['finished_at'] == conflict_data['finished_at']

    def test_delete(self):
        conflicts = baker.make(ArmedConflict, 3)

        req = self.client.get('/api/armed_conflicts/')
        assert len(req.json()) == 3

        self.client.delete(f'/api/armed_conflicts/{conflicts[0].id}/')
        req2 = self.client.get('/api/armed_conflicts/')
        assert len(req2.json()) == 2

    def test_update(self):
        conflict = baker.make(ArmedConflict)

        new_title = "Updated Conflict Title"
        req = self.client.put(f'/api/armed_conflicts/{conflict.id}/', {
            'title': new_title,
            'started_at': conflict.started_at.isoformat(),
            'finished_at': conflict.finished_at.isoformat() if conflict.finished_at else ''
        })
        assert req.status_code == 200

        req = self.client.get(f'/api/armed_conflicts/{conflict.id}/')
        assert req.json()['title'] == new_title


class AmmoTypesTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        ammo_type = baker.make(AmmoType)

        req = self.client.get('/api/ammo_types/')
        data = req.json()

        assert data[0]['title'] == ammo_type.title

    def test_post(self):
        ammo_data = {
            "title": "7.62x39mm",
        }

        req = self.client.post('/api/ammo_types/', ammo_data)
        data = req.json()

        assert data['title'] == ammo_data['title']

    def test_delete(self):
        ammo_types = baker.make(AmmoType, 4)

        req = self.client.get('/api/ammo_types/')
        assert len(req.json()) == 4

        self.client.delete(f'/api/ammo_types/{ammo_types[1].id}/')
        req2 = self.client.get('/api/ammo_types/')
        assert len(req2.json()) == 3

    def test_update(self):
        ammo_type = baker.make(AmmoType)
        new_title = 'Some new title'

        req = self.client.put(f'/api/ammo_types/{ammo_type.id}/', {
            'title': new_title,
        })
        assert req.status_code == 200

        req = self.client.get(f'/api/ammo_types/{ammo_type.id}/')
        assert req.json()['title'] == new_title


class ConstructorsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        constructor = baker.make(Constructor)

        req = self.client.get('/api/constructors/')
        data = req.json()

        assert data[0]['name'] == constructor.name
        assert data[0]['born_at'] == constructor.born_at.isoformat()

    def test_post(self):
        constructor_data = {
            "name": "Mikhail Kalashnikov",
            "born_at": "1919-11-10",
            "died_at": "2013-12-23"
        }

        req = self.client.post('/api/constructors/', constructor_data)
        data = req.json()

        assert data['name'] == constructor_data['name']
        assert data['born_at'] == constructor_data['born_at']
        assert data['died_at'] == constructor_data['died_at']

    def test_delete(self):
        constructors = baker.make(Constructor, 6)

        req = self.client.get('/api/constructors/')
        assert len(req.json()) == 6

        self.client.delete(f'/api/constructors/{constructors[4].id}/')
        req2 = self.client.get('/api/constructors/')
        assert len(req2.json()) == 5

    def test_update(self):
        constructor = baker.make(Constructor)

        new_name = "Updated Constructor Name"
        req = self.client.put(f'/api/constructors/{constructor.id}/', {
            'name': new_name,
            'born_at': constructor.born_at.isoformat(),
            'died_at': constructor.died_at.isoformat() if constructor.died_at else ''
        })
        assert req.status_code == 200

        req = self.client.get(f'/api/constructors/{constructor.id}/')
        assert req.json()['name'] == new_name


class TypeOfMountTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        mount = baker.make(TypeOfMount, title="Picatinny Rail")

        req = self.client.get('/api/type_of_mount/')
        data = req.json()

        assert data[0]['title'] == mount.title
        assert data[0]['id'] == mount.id

    def test_post(self):
        mount_data = {
            "title": "M-LOK"
        }

        req = self.client.post('/api/type_of_mount/', mount_data)
        data = req.json()

        assert data['title'] == mount_data['title']
        assert 'id' in data

    def test_delete(self):
        mounts = baker.make(TypeOfMount, 3)

        req = self.client.get('/api/type_of_mount/')
        assert len(req.json()) == 3

        self.client.delete(f'/api/type_of_mount/{mounts[1].id}/')
        req2 = self.client.get('/api/type_of_mount/')
        assert len(req2.json()) == 2

    def test_update(self):
        mount = baker.make(TypeOfMount, title="Old Mount")
        new_title = "New Picatinny Rail"

        req = self.client.put(f'/api/type_of_mount/{mount.id}/', {
            'title': new_title,
        })
        assert req.status_code == 200

        req = self.client.get(f'/api/type_of_mount/{mount.id}/')
        assert req.json()['title'] == new_title


class AttachmentTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        mount = baker.make(TypeOfMount)
        attachment = baker.make(Attachment, title="Red Dot Sight", type_of_mount=mount)

        req = self.client.get('/api/attachment/')
        data = req.json()

        assert data[0]['title'] == attachment.title
        assert data[0]['type_of_mount'] == mount.id

    def test_post(self):
        mount = baker.make(TypeOfMount)
        attachment_data = {
            "title": "Tactical Foregrip",
            "type_of_mount": mount.id
        }

        req = self.client.post('/api/attachment/', attachment_data)
        data = req.json()

        assert data['title'] == attachment_data['title']
        assert data['type_of_mount'] == mount.id

    def test_delete(self):
        mount = baker.make(TypeOfMount)
        attachments = baker.make(Attachment, 4, type_of_mount=mount)

        req = self.client.get('/api/attachment/')
        assert len(req.json()) == 4

        self.client.delete(f'/api/attachment/{attachments[2].id}/')
        req2 = self.client.get('/api/attachment/')
        assert len(req2.json()) == 3

    def test_update(self):
        mount = baker.make(TypeOfMount)
        attachment = baker.make(Attachment, title="Old Scope", type_of_mount=mount)
        new_title = "Advanced Tactical Scope"

        req = self.client.put(f'/api/attachment/{attachment.id}/', {
            'title': new_title,
            'type_of_mount': mount.id
        })
        assert req.status_code == 200

        req = self.client.get(f'/api/attachment/{attachment.id}/')
        assert req.json()['title'] == new_title


class LoadoutTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = baker.make(User, username="testuser")
        self.user_profile = self.user.userprofile

    def test_get_list(self):
        rifle = baker.make(Rifle)
        loadout = baker.make(Loadout, title="My AK-47 Build", rifle=rifle, creator=self.user_profile)

        req = self.client.get('/api/loadout/')
        data = req.json()

        assert data[0]['title'] == loadout.title
        assert data[0]['rifle'] == rifle.id
        assert data[0]['creator'] == self.user_profile.id

    def test_post(self):
        country = baker.make(Country)
        ammo = baker.make(AmmoType)
        rifle = baker.make(Rifle, country_of_origin=country, ammo_type=ammo)
        mount = baker.make(TypeOfMount)
        attachment = baker.make(Attachment, type_of_mount=mount)

        loadout_data = {
            "title": "Stealth Build",
            "rifle": rifle.id,
            "creator": self.user_profile.id,
            "attachments": [attachment.id]
        }

        req = self.client.post('/api/loadout/', loadout_data)
        data = req.json()

        assert data['title'] == loadout_data['title']
        assert data['rifle'] == rifle.id
        assert data['creator'] == self.user_profile.id
        assert attachment.id in data['attachments']

    def test_delete(self):
        rifle = baker.make(Rifle, country_of_origin=baker.make(Country), ammo_type=baker.make(AmmoType))
        loadouts = baker.make(Loadout, 3, rifle=rifle, creator=self.user_profile)

        req = self.client.get('/api/loadout/')
        assert len(req.json()) == 3

        self.client.delete(f'/api/loadout/{loadouts[1].id}/')
        req2 = self.client.get('/api/loadout/')
        assert len(req2.json()) == 2

    def test_update(self):
        rifle = baker.make(Rifle, country_of_origin=baker.make(Country), ammo_type=baker.make(AmmoType))
        loadout = baker.make(Loadout, title="Old Build", rifle=rifle, creator=self.user_profile)
        new_title = "Upgraded Stealth Build"

        req = self.client.put(f'/api/loadout/{loadout.id}/', {
            'title': new_title,
            'rifle': rifle.id,
            'creator': self.user_profile.id,
            'attachments': []
        })
        assert req.status_code == 200

        req = self.client.get(f'/api/loadout/{loadout.id}/')
        assert req.json()['title'] == new_title