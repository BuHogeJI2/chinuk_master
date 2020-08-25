from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.


def index(request):
    clinets = Client.objects.all()
    treners = Trener.objects.all()
    addresses = Address.objects.all()
    groups = Group.objects.all()
    payments = Payment.objects.all()

    return render(request, 'billing/index.html', {
        'clients': clinets,
        'treners': treners,
        'addresses': addresses,
        'groups': groups,
        'payments':payments,
    })

def detail_client(request, id):
    cli = Client.objects.get(id=id)
    groups = cli.groups.all()
    treners = cli.treners.all()
    payments = cli.payment_set.all()
    return render(request, 'billing/detail_client.html', {
        'client': cli,
        'groups': groups,
        'treners': treners,
        'payments': payments,
    })

def detail_group(request, id):
    group = Group.objects.get(id=id)
    group_clients = group.client_set.all()
    return render(request, 'billing/detail_group.html', {
        'group': group,
        'group_clients': group_clients,
    })

def add_new_client(request):
    return HttpResponse('HERE')