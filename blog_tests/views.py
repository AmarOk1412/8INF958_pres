# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    text = '8INF958 Basic demo'
    return HttpResponse(text)


def addition(request, nombre1, nombre2):
    total = int(nombre1) + int(nombre2)
    # Retourne nombre1, nombre2 et la somme des deux au tpl

    return render(request, 'addition.html', locals())
