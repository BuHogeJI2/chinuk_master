from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from .models import *
from .forms import *
from datetime import date, timedelta

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

def detail_payment(request, id):
    payment = Payment.objects.get(id=id)
    return render(request, 'billing/payment_detail.html', {
        'payment' : payment,
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

def total_payment(payments, date=date.today()):
    result = 0
    for payment in payments:
        if payment.date >= date:
            result += payment.amount

    return result

def get_report(request):
    payments = Payment.objects.all()
    return render(request, 'billing/report.html', {
        'payments': payments,
        'result' : total_payment(payments, date.today()),
    })


def add_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save()
            return redirect('detail_payment', payment.id)
    else:
        form = PaymentForm
    return render(request, 'billing/add_payment.html', {
        'form' : form,
    })