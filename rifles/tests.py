from django.test import TestCase
from model_bakery import baker
from rest_framework.test import APIClient

from rifles.models import Country, AmmoType, Constructor, ArmedConflict, Rifle


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
        country1 = baker.make(Country)
        country2 = baker.make(Country)
        conflict = baker.make(ArmedConflict)

        req = self.client.get('/api/armed_conflicts/')
        data = req.json()

        assert data[0]['title'] == conflict.title
        assert data[0]['started_at'] == conflict.started_at.isoformat()

    def test_post(self):
        country1 = baker.make(Country)

        conflict_data = {
            "title": "World War II",
            "started_at": "1939-09-01",
            "finished_at": "1945-09-02",
            "countries": [country1.id]
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
        country = baker.make(Country)
        conflict = baker.make(ArmedConflict)

        new_title = "Updated Conflict Title"
        req = self.client.put(f'/api/armed_conflicts/{conflict.id}/', {
            'title': new_title,
            'started_at': conflict.started_at.isoformat(),
            'finished_at': conflict.finished_at.isoformat() if conflict.finished_at else '',
            'countries': [country.id]
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
