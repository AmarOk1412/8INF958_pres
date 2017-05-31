# -*- coding: utf-8 -*-
from django.shortcuts import render
from leakntest.forms import EntryForm
from leakntest.models import Entry


def home(request):
    if request.method == 'POST':
        form = EntryForm(request.POST)

        if form.is_valid():
            # On envoie la requete vers la page 'search'
            entry = form.cleaned_data['entry']
            new_entry = Entry()
            filters = []
            if form.cleaned_data['search_name']:
                filters.append('search_name')
            if form.cleaned_data['search_mail']:
                filters.append('search_mail')
            if form.cleaned_data['search_password']:
                filters.append('search_password')
            if form.cleaned_data['search_hashword']:
                filters.append('search_hashword')
            if form.cleaned_data['search_website']:
                filters.append('search_website')
            query = new_entry.get_all_by_entry(entry, filters)
            return search(request, query)

    else:  # On est dans une requete GET
        form = EntryForm()  # On crée un formulaire vide

    return render(request, 'index.html', locals())


def search(request, entry):
    return render(request, 'search.html', locals())
