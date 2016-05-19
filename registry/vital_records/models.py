from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext as _

from .validators import non_zero_integer, birth_date_not_future

_gender_choices = (
    (True, _('Male')),
    (False, _('Female'))
)


class Residence(models.Model):
    postal_code = models.PositiveIntegerField('postal code')
    country = models.CharField('country', max_length=45)  # consider restriction
    region = models.CharField('region', max_length=64)
    district = models.CharField('district', max_length=64)
    city = models.CharField('city', max_length=64)
    street = models.CharField('street', max_length=64)
    house = models.CharField('house', max_length=45)
    room = models.CharField('room', max_length=45, blank=True)

    class Meta:
        verbose_name = _('Residence info')
        verbose_name_plural = _('Residences')


class Registrar(models.Model):
    name = models.CharField('name', max_length=255)
    residence = models.ForeignKey(Residence, on_delete=models.PROTECT)

    class Meta:
        verbose_name = _('Registrar')
        verbose_name_plural = _('Registrars')


class Note(models.Model):
    create_time = models.DateTimeField('note creation time', auto_now_add=True)
    compose_date = models.DateField('note record compose date', blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        editable=False
    )
    was_restored = models.BooleanField('was restored', default=False)
    was_revoked = models.BooleanField('was revoked', default=False)
    official_info = models.CharField('official info', max_length=255)
    notes = models.TextField(blank=True)
    language = models.CharField('language', max_length=45)  # convert to choices
    registrar = models.ForeignKey(Registrar, on_delete=models.PROTECT)


class ApplicantInfo(models.Model):
    first_name = models.CharField('first name', max_length=64)
    last_name = models.CharField('last name', max_length=64)
    patronymic = models.CharField('patronymic', max_length=64)
    residence = models.ForeignKey(Residence, on_delete=models.PROTECT)

    class Meta:
        verbose_name = _('Applicant information')
        verbose_name_plural = _('Applicants information')


class BirthPlace(models.Model):
    country = models.CharField('country', max_length=45)  # consider restriction
    region = models.CharField('region', max_length=64)
    district = models.CharField('district', max_length=64)
    city = models.CharField('city', max_length=64)

    class Meta:
        verbose_name = _('Birth place')
        verbose_name_plural = _('Birth places')


class Person(models.Model):
    first_name = models.CharField('first name', max_length=64)
    last_name = models.CharField('last name', max_length=64)
    patronymic = models.CharField('patronymic', max_length=64)
    gender = models.BooleanField('gender', choices=_gender_choices, default=False)
    residence = models.ForeignKey(Residence, on_delete=models.PROTECT)
    birth_place = models.ForeignKey(BirthPlace, on_delete=models.PROTECT)
    date_of_birth = models.DateField('date of birth')
    nationality = models.CharField('nationality', max_length=45, blank=True)
    family_status = models.BooleanField('family status')
    military_service = models.BooleanField('military service')

    class Meta:
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')


class Document(models.Model):  # too generic name, choose more appropriate
    title = models.CharField('title', max_length=45)
    series = models.CharField('series', max_length=45)
    number = models.CharField('number', max_length=45)
    issued_by = models.CharField('issued by organisation', max_length=45)
    issue_date = models.DateField('issue date')

    class Meta:
        verbose_name = _('Document')
        verbose_name_plural = _('Documents')


class RegistryUser(AbstractUser):
    registrar = models.ForeignKey(Registrar, on_delete=models.PROTECT, null=True)


class DeathPlace(models.Model):
    country = models.CharField('country', max_length=45)
    region = models.CharField('region', max_length=45)
    district = models.CharField('district', max_length=45)
    city = models.CharField('city', max_length=45)

    class Meta:
        verbose_name = _('Death place')
        verbose_name_plural = _('Death places')


class DeathEvidence(models.Model):
    title = models.CharField('title', max_length=64)
    number = models.CharField('number', max_length=32)
    issue_date = models.DateField('issue date')
    issuer = models.CharField('issuer', max_length=255)
    additional_info = models.TextField('additional info', blank=True)

    class Meta:
        verbose_name = _('Death evidence')
        verbose_name_plural = _('Death evidences')


class DeathNote(Note):
    note_number = models.PositiveIntegerField('note number')
    person = models.ForeignKey(Person, on_delete=models.PROTECT)
    applicant = models.ForeignKey(ApplicantInfo, on_delete=models.PROTECT)
    date_of_death = models.DateField('date of death')
    death_reason = models.TextField('reason of death', blank=True)
    rehabilitation_statements = models.CharField('rehabilitation statements', max_length=45)
    discarded_documents = models.OneToOneField(Document, on_delete=models.PROTECT)
    death_place = models.ForeignKey(DeathPlace, on_delete=models.PROTECT)
    death_evidence = models.ManyToManyField(DeathEvidence)

    class Meta:
        verbose_name = _('Death note record')
        verbose_name_plural = _('Death note records')


class MarriageNote(Note):
    note_number = models.PositiveIntegerField('note number')
    marriage_date = models.DateField('marriage date')
    husband = models.ForeignKey(Person, on_delete=models.PROTECT, related_name='male_marriages')
    wife = models.ForeignKey(Person, on_delete=models.PROTECT, related_name='female_marriages')

    class Meta:
        verbose_name = _('Marriage note record')
        verbose_name_plural = _('Marriage note records')


class BirthNoteLaw(models.Model):
    law = models.CharField('law', max_length=255)

    class Meta:
        verbose_name = _('Birth related law')
        verbose_name_plural = _('Birth related laws')


class BirthEvidence(models.Model):
    title = models.CharField('title', max_length=64)
    number = models.CharField('number', max_length=32)
    issue_date = models.DateField('issue date')
    issuer = models.CharField('issued by organisation', max_length=255, blank=True)

    class Meta:
        verbose_name = _('Birth evidence')
        verbose_name_plural = _('Birth evidences')


class BirthNote(Note):
    def clean(self):
        if self.child_number > self.children_born_count:
            raise ValidationError(_("Child number can't be larger than child born count"))
        super().clean()

    note_number = models.PositiveIntegerField('note number')
    deadline_passed = models.BooleanField('deadline passed')
    applicant = models.ForeignKey(ApplicantInfo, on_delete=models.PROTECT)
    law = models.ForeignKey(BirthNoteLaw, on_delete=models.PROTECT)
    stillborn = models.BooleanField('stillborn')
    children_born_count = models.PositiveIntegerField(
        'children born count',
        validators=[
            non_zero_integer(_("Children born count can't be zero"))
        ]
    )
    child_number = models.PositiveIntegerField(
        'child number',
        validators=[
            non_zero_integer(_("Child number can't be zero"))
        ]
    )
    birth_date = models.DateField('date of birth', validators=[birth_date_not_future])
    birth_place = models.ForeignKey(BirthPlace, on_delete=models.PROTECT)
    birth_evidences = models.ManyToManyField(BirthEvidence)
    child_gender = models.BooleanField('gender', choices=_gender_choices, default=False)
    child_name = models.CharField('name', max_length=64)
    child_last_name = models.CharField('last name', max_length=64)
    child_patronymic = models.CharField('patronymic', max_length=64)
    parents = models.ManyToManyField(Person)
    father_info_reason = models.TextField('father info reason')

    class Meta:
        verbose_name = _('Birth note record')
        verbose_name_plural = _('Birth note records')
