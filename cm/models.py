# -*- coding: utf-8 -*-

import urllib
import hashlib
import random
import string
import os

from django.db import models
import django.contrib.auth.models


class Configuration(models.Model):
    name = models.CharField(max_length=100, unique=True)
    value = models.CharField(max_length=100)
    default = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name + ': ' + self.value


class PaperType(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Keyword(models.Model):
    name = models.CharField(max_length=100)
    parentKeyword = models.ForeignKey('self', related_name='SubKeyword', blank=True, null=True)

    def __unicode__(self):
        return self.name

# um die PaperID mit zu integrieren:
# http://stackoverflow.com/questions/9968532/django-admin-file-upload-with-current-model-id
def get_upload_filename(instance, filename):
    return 'papers/{conf_abbr}_{pk}_{random_string}.{extension}'.format(
        conf_abbr=Configuration.objects.get(name='conf_abbr').value,
        pk=instance.pk,
        random_string=''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32)),
        extension=os.path.splitext(filename)[1][1:])


class Paper(models.Model):
    title = models.CharField(max_length=125)
    abstract = models.TextField()
    submissionDate = models.DateTimeField(auto_now_add=True)
    paperType = models.ForeignKey(PaperType)
    paperFile = models.FileField(upload_to=get_upload_filename)

    def __unicode__(self):
        return self.title

    # um die PaperID in den Filename zu integrieren:
    # http://stackoverflow.com/questions/9968532/django-admin-file-upload-with-current-model-id
    def save(self, *args, **kwargs):
        if self.pk is None:
            saved_paperFile = self.paperFile
            self.paperFile = None
            super(Paper, self).save(*args, **kwargs)
            self.paperFile = saved_paperFile
        super(Paper, self).save(*args, **kwargs)


django.contrib.auth.models.User._meta.get_field('email')._unique = True

# ToDo: User Model umstellen vgl. Django 1.6
class UserProfile(models.Model):
    user = models.OneToOneField(django.contrib.auth.models.User, unique=True)
    affiliation1 = models.CharField(max_length=50, help_text='university etc.')
    affiliation2 = models.CharField(max_length=50, help_text='institute etc.', blank=True)
    town = models.CharField(max_length=50, blank=True)
    zip = models.CharField(max_length=10, blank=True)
    gravatar = models.CharField(max_length=100, blank=True)
    # TODO: Countries einfuegen
    # country = models.ForeignKey(country)
    phone1 = models.CharField(max_length=20, blank=True)
    url = models.URLField(blank=True)
    LANGUAGE_CHOICES = (('DE', 'deutsch'), ('EN', 'english'))
    timezone = models.CharField(max_length=50, default='Europe/Berlin', help_text='for customization')
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, blank=True)

    class Meta:
        ordering = ['user']

    def save(self):
        self.gravatar = generate_gravatar(self.user.email)
        self.user.save()
        super(UserProfile, self).save()
        return

    def __unicode__(self):
        return u"{full_name} (#{pk}/{pk_user})".format(full_name=self.user.get_full_name(),
                                                    pk=self.pk,
                                                    pk_user=self.user.pk)

# generate gravatar icon
def generate_gravatar(email, default="identicon", size=20):
    return "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?" \
           + urllib.urlencode({'d': default, 's': str(size)})


# Todo: Validator, der prueft, ob es die email-Adresse schon bei User gibt
class AdditionalEmail(models.Model):
    email = models.EmailField(max_length=50, unique=True)
    user_profile = models.ForeignKey(UserProfile, related_name='additional_emails')

    def __unicode__(self):
        return self.email

    # Prüfe, ob es die email-Adresse schon gibt, ggf. ignorieren
    def save(self):
        # Todo: Fehlermeldung ausgeben, wenn ein anderer Nutzer die Email-Adresse bereits nutzt
        # Speichere nur, wenn es die Adresse nicht schon gibt
        if not django.contrib.auth.models.User.objects.filter(email=self.email).exists():
            self.user.save()
            super(UserProfile, self).save()
        return


# Für das Formular http://stackoverflow.com/questions/698301/is-there-a-native-jquery-function-to-switch-elements
class Author(models.Model):
    order = models.PositiveSmallIntegerField()
    isContactAuthor = models.BooleanField(default=False)
    paper = models.ForeignKey(Paper)
    person = models.ForeignKey(UserProfile)

    class Meta:
        unique_together = ('person', 'paper')
        ordering = ['order']


# TODO: brauchen wir wahrscheinlich nicht, ggf. loeschen
# objects = django.contrib.auth.models.UserManager()

