from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.


def index(request):
    clinets = Client.objects.all()
    treners = Trener.objects.all()
    addresses = Address.objects.all()
    groups = Group.objects.all()

    return render(request, 'billing/index.html', {
        'clients': clinets,
        'treners': treners,
        'addresses': addresses,
        'groups': groups,
    })

def detail_client(request, id):
    cli = Client.objects.get(id=id)
    groups = cli.groups.all()
    treners = cli.treners.all()
    return render(request, 'billing/detail_client.html', {
        'client': cli,
        'groups': groups,
        'treners': treners,
    })