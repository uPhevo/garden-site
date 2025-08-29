from django.shortcuts import render
from flowers.models import Flower, Category, About, Contact, WorkCondition

def home(request):
    return render(request, 'main/home.html')


def catalog(request):
    categories = Category.objects.all()
    flowers = Flower.objects.all()
    return render(request, 'main/catalog.html', {
        'categories': categories,
        'flowers': flowers
    })


def about(request):
    # Берём первую запись из модели About
    about = About.objects.first()
    return render(request, 'main/about.html', {'about': about})


def contacts(request):
    # Берём первую запись из модели Contact
    contacts = Contact.objects.first()
    return render(request, 'main/contacts.html', {'contacts': contacts})


def personals(request):
    # Берём первую запись из модели WorkCondition
    conditions = WorkCondition.objects.first()
    return render(request, 'main/personals.html', {'conditions': conditions})
