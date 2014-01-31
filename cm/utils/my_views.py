# -*- coding: utf-8 -*-
__author__ = 'preuss'

from django.views.generic import View, ListView, DeleteView, CreateView, UpdateView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages

# http://www.nullege.com/codes/show/src%40d%40j%40django-bootstrap-0.2.4%40bootstrap%40views.py/133/django.views.generic.edit.DeleteView.get_object/python

class MyListView(ListView):
    def get_context_data(self, **kwargs):
        ctx = super(ListView, self).get_context_data(**kwargs)
        queryset = super(ListView, self).get_queryset().order_by(self.request.GET.get('sort_by', 'id'))
        paginator = Paginator(queryset, 10)
        try:
            show_rows = paginator.page(self.request.GET.get('page'))
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            show_rows = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            show_papers = paginator.page(paginator.num_pages)
        ctx['rows'] = show_rows
        ctx['queryset'] = queryset
        return ctx
    # customize the queryset
    #def get_queryset(self):
    #    """ Redefinition of QuerySet to filter by current user. """
    #    return Constance.objects.all()


class MyDeleteView(DeleteView):
    def delete(self, *args, **kwargs):
        instance = self.get_object()
        messages.success(self.request, self.get_success_message())
        return super(DeleteView, self).delete(*args, **kwargs)

    def get_success_message(self):
        return  u'Successfully deleted.'

class MyDeleteViewWithoutConfirm(MyDeleteView):
    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

class MyCreateView(CreateView):
    title = ''
    def get_context_data(self, **kwargs):
        ctx = super(CreateView, self).get_context_data(**kwargs)
        ctx['title'] = self.title
        return ctx

class MyUpdateView(UpdateView):
    title = ''
    def get_context_data(self, **kwargs):
        ctx = super(UpdateView, self).get_context_data(**kwargs)
        ctx['title'] = self.title
        return ctx

    def get_success_message(self):
        return  u'Successfully updated.'

class MyView(View):
    title = ''
    def get_context_data(self, **kwargs):
        ctx = super(UpdateView, self).get_context_data(**kwargs)
        ctx['title'] = self.title
        return ctx

    def get_success_message(self):
        return  u'Successfully updated.'
