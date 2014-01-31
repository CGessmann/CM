# -*- coding: utf-8 -*-

from django.forms import *
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory, modelformset_factory


from .models import *
from .utils.helper import unique_field_formset


__author__ = 'Thomas Preuss'


class PaperForm(ModelForm):
    class Meta:
        model = Paper
        exclude = ['submissionDate']


class UserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for f in ('first_name', 'last_name', 'email'):
            self.fields[f].required = True

    class Meta:
        model = User
        widgets = {'password': PasswordInput(),
                   'first_name': TextInput(attrs={'title': 'I am "nice"'}),
                   'email': TextInput(attrs={'label': 'Correspondence email address'}),
                   }
        fields = ['first_name', 'last_name', 'username', 'email']


class UserProfileForm(ModelForm):
    language = ChoiceField(widget=RadioSelect(attrs={'data-demo-attr': 'bazinga'}),
                           choices=UserProfile.LANGUAGE_CHOICES,
                           help_text='la')

    class Meta:
        model = UserProfile
        exclude = ['user', 'gravatar']


class AdditionalEmailForm(ModelForm):
    class Meta:
        model = AdditionalEmail

AdditionalEmailFormset = inlineformset_factory(parent_model=UserProfile, model= AdditionalEmail,
                                        formset=unique_field_formset('email'),
                                        can_delete=False, can_order=False, max_num=6, extra=1)

AdditionalEmailFormsetModel = modelformset_factory(AdditionalEmail,
                                        formset=unique_field_formset('email'),
                                        can_delete=False, can_order=False, max_num=6, extra=1)


class AuthorForm(ModelForm):
    class Meta:
        model = Author
