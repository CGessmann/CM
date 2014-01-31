# -*- coding: utf-8 -*-

__author__ = 'preuss'

from django.forms import *
from cm.models import Configuration
from django.contrib.auth.models import User

def get_config(name, default):
    value = Configuration.objects.get(name=name).value
    return value if value else default

# https://djangosnippets.org/snippets/2816/
# Todo: Funktioniert nicht: da nicht geprüft wird, ob es in User und AddForm Dopplungen gibt
# Evtl. sollten wir die zusätzlichen Email-Adressen hier rausnehmen und sie nur
# in der Detailansicht bzw. beim Mergen dazu nehmen.
def unique_field_formset(field_name):
    from django.forms.models import BaseInlineFormSet

    class UniqueFieldFormSet(BaseInlineFormSet):
        def clean(self):
            if any(self.errors):
                # Don't bother validating the formset unless each form is valid on its own
                return
            values = set()
            for form in self.forms:
                value = form.cleaned_data.get(field_name)
                if value and (value in values): # check for duplicate entries in the same formset
                    raise forms.ValidationError(u'Duplicate values ({value}) for {field_name} are not allowed.'
                                                    .format(field_name=field_name, value=value))
                if User.objects.filter(email=value).exists(): # check for already existing email addresses
                    raise forms.ValidationError(u'A {field_name} {value} already exists.'
                                                    .format(field_name=field_name, value=value))
                values.add(value)

    return UniqueFieldFormSet
