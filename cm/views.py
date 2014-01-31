# -*- coding: utf-8 -*-

from django.shortcuts import *
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from jsonview.decorators import json_view
from django.views.generic import FormView
from django.core.urlresolvers import reverse_lazy

from .forms import *
from utils.my_views import *


class AdditionalEmailForm(ModelForm):
    class Meta:
        model = AdditionalEmail
        exclude = ['user_profile']


class PersonView(View):
    # wird bei jedem GET/POST als erstes aufgerufen, danach kommt get() bzw. post()
    # aus der urls.py können nur Klassenattribute übergeben werden, daher der WorkAround
    pk = title = success_url = cancel_url = None
    def dispatch(self, request, *args, **kwargs):
        self.template_name = kwargs.get('template_name', u'cm/person_view.html')
        self.title = kwargs.get('title', u'Edit Person Data')
        self.success_url = kwargs.get('cancel_url', u'personList')
        self.cancel_url = kwargs.get('cancel_url', u'personList')
        pk = kwargs.get('pk')
        if pk == None:
            self.user_profile = UserProfile()
            self.user = User()
        else:
            self.user_profile = get_object_or_404(UserProfile, pk=pk)
            self.user = self.user_profile.user

        # BAstle die Formset-Klasse für die Additional Email Addresses zusammen
        self.AdditionalEmailFormset = inlineformset_factory(UserProfile, AdditionalEmail, form=AdditionalEmailForm,
                                                            formset=unique_field_formset('email'),
                                                            can_delete=False, can_order=False, max_num=6, extra=6)

        # Weiter mit dem normalen Ablauf
        return super(PersonView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
    # Befülle die Forms mit leeren bzw. gespeicherten Objekten
        self.user_profile_form = UserProfileForm(instance=self.user_profile)
        self.user_form = UserForm(instance=self.user)
        self.additional_email_formset = self.AdditionalEmailFormset(instance=self.user_profile)

        return self.render_form(request)

    def post(self, request, *args, **kwargs):
        self.user_profile_form = UserProfileForm(request.POST, instance=self.user_profile)
        self.user_form = UserForm(request.POST, instance=self.user)
        self.additional_email_formset = self.AdditionalEmailFormset(request.POST, instance=self.user_profile)

        if self.user_form.is_valid() and self.user_profile_form.is_valid() and self.additional_email_formset.is_valid():
            for i in self.additional_email_formset:
                print i
            saved_user = self.user_form.save()
            user_profile = self.user_profile_form.save(commit=False)
            user_profile.user = saved_user
            self.user_profile_form.save()
            self.additional_email_formset.save()
            messages.success(request, u'Person data saved.')
            return HttpResponseRedirect(reverse(self.success_url))
        else:
            messages.error(request, u'Please check the data below.')

        return self.render_form(request)


    def render_form(self, request):
        return render_to_response(self.template_name,
                                  RequestContext(request, {'user_form': self.user_form,
                                                           'additional_email_formset': self.additional_email_formset,
                                                           'user_profile_form': self.user_profile_form,
                                                           'title': self.title,
                                                           'cancel_url': reverse(self.cancel_url),
                                  }))


class UserProfileDelete(MyDeleteView):
    model = User
    success_url = reverse_lazy('personList')

    def get_success_message(self):
        return u'The person "{full_name}" (#{pk}) has been deleted.'.format(full_name=self.get_object().get_full_name(),
                                                                            pk=self.get_object().pk)


class PaperDelete(MyDeleteView):
    model = Paper
    success_url = reverse_lazy('paperList')

    def get_success_message(self):
        return u'The paper "{title}" (#{pk}) has been deleted.'.format(title=self.get_object().title,
                                                                       pk=self.get_object().pk)

class PaperView(View):
    # wird bei jedem GET/POST als erstes aufgerufen, danach kommt get() bzw. post()
    # aus der urls.py können nur Klassenattribute übergeben werden, daher der WorkAround
    pk = title = success_url = cancel_url = None
    def dispatch(self, request, *args, **kwargs):
        self.context = {}
        self.context['title'] = kwargs.get('title', u'Edit Paper Data')
        self.context['cancel_url'] = kwargs.get('cancel_url', u'paperList')
        self.success_url = kwargs.get('cancel_url', u'paperList')
        self.template_name = kwargs.get('template_name', u'cm/paper_view.html')
        pk = kwargs.get('pk')
        if pk == None:
            self.paper = Paper()
        else:
            self.paper = get_object_or_404(Paper, pk=pk)

        # Weiter mit dem normalen Ablauf
        return super(PaperView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
    # Befülle die Forms mit leeren bzw. gespeicherten Objekten
        self.paper_form = PaperForm(instance=self.paper)
        return self.render_form(request)

    def post(self, request, *args, **kwargs):
        self.paper_form = PaperForm(request.POST, instance=self.paper)

        if self.paper_form.is_valid():
            self.paper_form.save()
            messages.success(request, u'Paper data saved.')
            return HttpResponseRedirect(reverse(self.success_url))
        else:
            messages.error(request, u'Please check the data below.')

        return self.render_form(request)


    def render_form(self, request):
        self.context['paper_form'] = self.paper_form
        return render_to_response(self.template_name, RequestContext(request, self.context))


def paper_view(request, paperID=None):
    AuthorFormset = inlineformset_factory(Paper, Author, form=AuthorForm,
                                          can_delete=False, can_order=False, max_num=6, extra=6)
    if paperID is None:
        title = 'Register New Paper'
        paper = Paper()
    else:
        title = 'Edit Paper'
        paper = get_object_or_404(Paper, pk=paperID)

    if request.method == 'POST':
        form = PaperForm(request.POST, request.FILES, instance=paper)
        if form.is_valid():
            form.save()
            messages.success(request, u'Paper successfully saved.')
            return HttpResponseRedirect(reverse('cm.views.paper_list'))
        else:
            messages.error(request, 'Please check the data below.')
    else:
        form = PaperForm(instance=paper)
    return render_to_response('cm/paper_view.html', RequestContext(request, {'form': form,
                                                                             'title': title,
                                                                             'cancel_url': reverse(
                                                                                 'paperList')}))


def password_reset_done(request):
    messages.success(request, u'Password changed. Please login again.')
    return HttpResponseRedirect(reverse('login'))


# hier noch Rechtepruefung einfuegen
def su(request, pk=None):
    try:
        pk = int(pk)
    except:
        pass
        # Man kann nicht man selbst werden
    if request.user.pk == pk:
        messages.error(request, u'You can not turn into yourself.')
    else:
        # Ist bereits im SuperuserMode, dann wechsle in die urspruengliche Identitaet
        if request.session.get('originalPersonID', None):
            user = get_object_or_404(User, pk=request.session.get('originalPersonID'))
            messages.success(request, u'Back to your original identity ({}).'.format(user.get_full_name()))
            del request.session['originalPersonID']
            originalPersonID = None
        else:
            # Versuche die Person zu finden und nimm ihre Identitaet an
            user = get_object_or_404(User, pk=pk)
            messages.success(request,
                             u'Turned into {}. To turn back to your original identity click on the icon in the footer.'.
                             format(user.get_full_name()))
            originalPersonID = request.user.pk

        # Workaround, da sonst login nicht funktioniert
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        # save the originalPersonID in the new SessionStore
        login(request, user)
        request.session['originalPersonID'] = originalPersonID
    return HttpResponseRedirect(reverse('start'))


@json_view
def get_affiliation(request):
    return [u.affiliation1 for u in
            UserProfile.objects.filter(affiliation1__icontains=request.GET.get('query')).
            only('affiliation1').order_by('affiliation1')]