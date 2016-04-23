from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Residence(models.Model):
    postal_code = models.PositiveIntegerField('postal code')
    country = models.CharField('country', max_length=45)  # consider restriction
    region = models.CharField('region', max_length=64)
    district = models.CharField('district', max_length=64)
    city = models.CharField('city', max_length=64)
    street = models.CharField('street', max_length=64)
    house = models.CharField('house', max_length=45)
    room = models.CharField('room', max_length=45, blank=True)


class Registrar(models.Model):
    name = models.CharField('name', max_length=255)
    residence = models.ForeignKey(Residence, on_delete=models.PROTECT)


class Note(models.Model):
    create_time = models.DateTimeField('note creation time', auto_now_add=True)
    compose_date = models.DateField('note record compose time', blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    was_restored = models.BooleanField('was restored', default=False)
    official_info = models.CharField('official info', max_length=255)
    # probably need choices see: https://docs.djangoproject.com/en/1.9/ref/models/fields/#choices
    status = models.CharField('status', max_length=45)
    notes = models.TextField(blank=True)
    language = models.CharField('language', max_length=45)  # convert to choices
    registrar = models.ForeignKey(Registrar, on_delete=models.PROTECT)


class ApplicantInfo(models.Model):
    name = models.CharField('name', max_length=64)
    last_name = models.CharField('last_name', max_length=64)
    patronymic = models.CharField('patronymic', max_length=64)
    residence = models.ForeignKey(Residence, on_delete=models.PROTECT)


class BirthPlace(models.Model):
    country = models.CharField('country', max_length=45)  # consider restriction
    region = models.CharField('region', max_length=64)
    district = models.CharField('district', max_length=64)
    city = models.CharField('city', max_length=64)


class Person(models.Model):
    name = models.CharField('name', max_length=64)
    last_name = models.CharField('last name', max_length=64)
    patronymic = models.CharField('patronymic', max_length=64)
    gender = models.BooleanField('gender')
    residence = models.ForeignKey(Residence, on_delete=models.PROTECT)
    birth_place = models.ForeignKey(BirthPlace, on_delete=models.PROTECT)
    date_of_birth = models.DateField('date of birth')
    nationality = models.CharField('nationality', max_length=45, blank=True)
    family_status = models.BooleanField('family status')
    military_service = models.BooleanField('military service')


class Document(models.Model):  # too generic name, choose more appropriate
    title = models.CharField('title', max_length=45)
    series = models.CharField('series', max_length=45)
    number = models.CharField('number', max_length=45)
    issued_by = models.CharField('issued by organisation', max_length=45)
    issue_date = models.DateField('issue date')


class RegistryUser(AbstractUser):
    registrar = models.ForeignKey(Registrar, on_delete=models.PROTECT, null=True)


class DeathPlace(models.Model):
    country = models.CharField('country', max_length=45)
    region = models.CharField('region', max_length=45)
    district = models.CharField('district', max_length=45)
    city = models.CharField('city', max_length=45)


class DeathEvidence(models.Model):
    title = models.CharField('title', max_length=64)
    number = models.CharField('number', max_length=32)
    issue_date = models.DateField('issue date')
    issuer = models.CharField('issuer', max_length=255)
    additional_info = models.TextField('additional info', blank=True)


class DeathNote(Note):
    person = models.ForeignKey(Person, on_delete=models.PROTECT)
    date_of_death = models.DateField('date of death')
    death_reason = models.TextField('reason of death', blank=True)
    rehabilitation_statements = models.CharField('rehabilitation statements', max_length=45)
    discarded_documents = models.ForeignKey(Document, on_delete=models.PROTECT)
    death_place = models.ForeignKey(DeathPlace, on_delete=models.PROTECT)
    death_evidence = models.ManyToManyField(DeathEvidence)


class MarriageNote(Note):
    note_number = models.PositiveIntegerField('note number')
    marriage_date = models.DateField('marriage date')
    husband = models.ForeignKey(Person, on_delete=models.PROTECT)
    wife = models.ForeignKey(Person, on_delete=models.PROTECT)


class BirthNoteLaw(models.Model):
    law = models.CharField('law', max_length=255)


class BirthEvidence(models.Model):
    title = models.CharField('title', max_length=64)
    number = models.CharField('number', max_length=32)
    issue_date = models.DateField('issue date')
    issuer = models.CharField('issued by organisation', max_length=255, blank=True)


class BirthNote(Note):
    note_number = models.PositiveIntegerField('note number')
    deadline_passed = models.BooleanField('deadline passed')
    law = models.ForeignKey(BirthNoteLaw, on_delete=models.PROTECT)
    stillborn = models.BooleanField('stillborn')
    children_born_count = models.PositiveIntegerField('children born count')
    child_number = models.PositiveIntegerField('children number')
    birth_date = models.DateField('date of birth')
    birth_place = models.ForeignKey(BirthPlace, on_delete=models.PROTECT)
    birth_evidences = models.ManyToManyField(BirthEvidence)
    child_gender = models.BooleanField('gender')
    child_name = models.CharField('name', max_length=64)
    child_last_name = models.CharField('last name', max_length=64)
    child_patronymic = models.CharField('patronymic', max_length=64)
    parents = models.ManyToManyField(Person)
    father_info_reason = models.TextField('father info reason')
    military_service = models.BooleanField('military service')  # questionable
