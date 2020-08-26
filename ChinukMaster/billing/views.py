from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *

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

    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save()
            return redirect('detail_client', id=client.id)
    else:
        form = ClientForm()
    return render(request, 'billing/new_client.html', {
        'form' : form,
    })

def find_client(request):

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            searching_card = request.POST['search_field']
            clients = Client.objects.filter(member_card__contains=f'{searching_card}')
            if clients:
                if len(clients) > 1:
                    return HttpResponse('Find more than 2 cards!!!')
                return redirect('detail_client', id=clients[0].id)
                print(clients)
            else:
                result = 'none'
                return render(request, 'billing/find_client.html', {
                    'form' : form,
                    'result': result,
                })
    else:
        form = SearchForm()
    return render(request, 'billing/find_client.html', {
        'form' : form,
    })