# -*- coding: utf-8 -*-
from django.shortcuts import render
from leakntest.forms import EntryForm
from leakntest.models import Entry


# Create your views here.
def home(request):
    if request.method == 'POST':
        form = EntryForm(request.POST)

        if form.is_valid():
            # On envoie la requete vers la page 'search'
            entry = form.cleaned_data['entry']
            return search(request, entry)

    else:  # On est dans une requete GET
        form = EntryForm()  # On crée un formulaire vide

    return render(request, 'index.html', locals())


def search(request, entry):
    new_entry = Entry()
    print(new_entry.get_all_by_entry(entry))
    return render(request, 'search.html', locals())
