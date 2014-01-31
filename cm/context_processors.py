# -*- coding: utf-8 -*-
__author__ = 'preuss'

from cm.models import Configuration


# http://catherinetenajeros.blogspot.de/2013/03/custom-template-context-processors.html
def configuration(request):
    return {parameter.name:parameter.value for parameter in Configuration.objects.filter()}
