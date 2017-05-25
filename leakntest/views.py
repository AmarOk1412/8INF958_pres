from django.shortcuts import render
from leakntest.forms import EntryForm


# Create your views here.
def home(request):
    if request.method == 'POST':
        form = EntryForm(request.POST)

        if form.is_valid():
            # On envoie la requête vers la page 'search'
            entry = form.cleaned_data['entry']
            return search(request, entry)

    else:  # On est dans une requête GET
        form = EntryForm()  # On crée un formulaire vide

    return render(request, 'index.html', locals())


def search(request, entry):
    return render(request, 'search.html', locals())
