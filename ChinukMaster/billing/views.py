from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.


def test(request):
    clinets = Client.objects.all()
    treners = Trener.objects.all()
    addresses = Address.objects.all()
    groups = Group.objects.all()

    return render(request, 'billing/test.html', {
        'clients': clinets,
        'treners': treners,
        'addresses': addresses,
        'groups': groups,
    })