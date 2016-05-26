from contextlib import contextmanager

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from .models import Person, Residence, RegistryUser, Registrar
from .models import BirthNote, BirthPlace, ApplicantInfo, BirthNoteLaw, BirthEvidence


class TestCaseExt:
    """TestCase extension methods"""
    @contextmanager
    def assertDoesntRaise(self, cls):
        """Check that code section doesn't throw an exception"""
        try:
            yield
        except cls:
            self.fail(cls.__name__ + ' has been raised')


class BirthNoteIntegrationTests(TestCase):
    def test_create_hierarchy(self):
        home = Residence.objects.create(
            postal_code=1024, country='UA', region='Kyivska oblast', district='Obukhivskiy',
            city='Obukhiv', street='Long', house=13, room=37
        )
        self.assertIsNotNone(home)

        father_birth_place = BirthPlace.objects.create(
            country='UA', region='Volynska oblast', district='Old republic', city='Urbanstadt'
        )
        self.assertIsNotNone(father_birth_place)
        father = Person.objects.create(
            first_name='Ivan', last_name='Ivanov', patronymic='Ivanovich',
            gender=Person.MALE, residence=home, birth_place=father_birth_place,
            date_of_birth=timezone.datetime(year=1970, month=3, day=5).date(),
            family_status=Person.MARRIED, military_service=False
        )
        self.assertIsNotNone(father)

        mother_birth_place = BirthPlace.objects.create(
            country='UA', region='Chernihivska oblast', district='Rare gems', city='Golden rain'
        )
        self.assertIsNotNone(mother_birth_place)
        mother = Person.objects.create(
            first_name='Anna', last_name='Ivanova', patronymic='Mikhailivna',
            gender=Person.FEMALE, residence=home, birth_place=mother_birth_place,
            date_of_birth=timezone.datetime(year=1975, month=7, day=21).date(),
            family_status=Person.MARRIED, military_service=True
        )
        self.assertIsNotNone(mother)

        applicant_residence = Residence.objects.create(
            postal_code=256, country='UA', region='Kyivska oblast', district='Solomyanskiy',
            city='Kyiv', street='Vandy Vasilevskoi', house=50, room=2
        )
        self.assertIsNotNone(applicant_residence)
        applicant = ApplicantInfo.objects.create(
            first_name='John', last_name='Doe', patronymic='Henry', residence=applicant_residence
        )
        self.assertIsNotNone(applicant)

        law = BirthNoteLaw.objects.create(law='Law #133 for some birth-related case')
        self.assertIsNotNone(law)

        child_birth_place = BirthPlace.objects.create(
            country='UA', region='Kyivska oblast', district='Obukhivskiy', city='Obukhiv'
        )
        self.assertIsNotNone(child_birth_place)

        birth_evidences = (
            BirthEvidence.objects.create(
                title='Important evidence', number=4352,
                issue_date=timezone.now().date(), issuer='Issuer info goes here'
            ),
            BirthEvidence.objects.create(
                title='Other evidence', number=845,
                issue_date=timezone.now().date() - timezone.timedelta(days=1), issuer='Some issuer'
            )
        )
        self.assertTrue(all(birth_evidences))

        registrar_residence = Residence.objects.create(
            postal_code=1024, country='UA', region='Kyivska oblast', district='Obukhivskiy',
            city='Obukhiv', street='Long', house=13, room=37
        )
        self.assertIsNotNone(registrar_residence)
        registrar = Registrar.objects.create(name='Registrar name', residence=registrar_residence)
        self.assertIsNotNone(registrar)

        note_author = RegistryUser.objects.create_user('test', 'local@email.here', 'test-user')
        self.assertIsNotNone(note_author)

        note = BirthNote.objects.create(
            compose_date=timezone.now().date(), created_by=note_author,
            registrar=registrar, official_info='Very important person', language='Ukrainian',
            note_number=65535, deadline_passed=False, applicant=applicant, law=law, stillborn=False,
            children_born_count=2, child_number=1,
            birth_date=timezone.now().date() - timezone.timedelta(days=1),
            birth_place=child_birth_place,
            child_gender=Person.FEMALE, child_name='jane', child_last_name='Ivanova',
            child_patronymic='Ivanovna',
            father_info_reason='Nothing'
        )
        note.parents.add(father, mother)
        note.birth_evidences.add(*birth_evidences)

        self.assertIsNotNone(note)
        self.assertEqual(note, BirthNote.objects.first())


class BirthNoteValidationTests(TestCase, TestCaseExt):
    fixtures = ['common', 'birth_note']

    def test_child_number_not_less_child_count(self):
        n = BirthNote.objects.first()
        n.children_born_count = 2
        n.child_number = 3
        with self.assertRaises(ValidationError):
            n.full_clean()
        n.child_number = 0
        with self.assertRaises(ValidationError):
            n.full_clean()
        n.child_number = 2
        with self.assertDoesntRaise(ValidationError):
            n.full_clean()

    def test_child_birth_date_not_future(self):
        n = BirthNote.objects.first()
        n.compose_date = timezone.now().date()
        n.birth_date = timezone.now().date()
        with self.assertDoesntRaise(ValidationError):
            n.full_clean()
        n.birth_date = timezone.now().date() + timezone.timedelta(days=1)
        with self.assertRaises(ValidationError):
            n.full_clean()
        n.birth_date = timezone.now().date() - timezone.timedelta(days=1)
        with self.assertDoesntRaise(ValidationError):
            n.full_clean()
        n.compose_date = timezone.now().date() - timezone.timedelta(days=1)
        with self.assertDoesntRaise(ValidationError):
            n.full_clean()
        n.birth_date = timezone.now().date()
        with self.assertRaises(ValidationError):
            n.full_clean()

    def test_children_count_greater_than_zero(self):
        n = BirthNote.objects.first()
        n.children_born_count = -1
        with self.assertRaises(ValidationError):
            n.full_clean()
        n.children_born_count = 0
        with self.assertRaises(ValidationError):
            n.full_clean()
        n.children_born_count = 1
        with self.assertDoesntRaise(ValidationError):
            n.full_clean()

    def test_compose_date_cant_be_future(self):
        n = BirthNote.objects.first()
        n.compose_date = timezone.now().date()
        with self.assertDoesntRaise(ValidationError):
            n.full_clean()
        n.compose_date = timezone.now().date() + timezone.timedelta(days=1)
        with self.assertRaises(ValidationError):
            n.full_clean()
        n.compose_date = timezone.now().date() - timezone.timedelta(days=1)
        with self.assertDoesntRaise(ValidationError):
            n.full_clean()



