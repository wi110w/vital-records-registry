from contextlib import contextmanager

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from .models import BirthNote


class TestCaseExt:
    """TestCase extension methods"""
    @contextmanager
    def assertDoesntRaise(self, cls):
        """Check that code section doesn't throw an exception"""
        try:
            yield
        except cls:
            self.fail(cls.__name__ + ' has been raised')


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
        n.birth_date = timezone.now().date()
        with self.assertRaises(ValidationError):
            n.full_clean()
        n.birth_date = timezone.now().date() + timezone.timedelta(days=1)
        with self.assertRaises(ValidationError):
            n.full_clean()
        n.birth_date = timezone.now().date() - timezone.timedelta(days=1)
        with self.assertDoesntRaise(ValidationError):
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



