from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse, Http404
from django.utils import timezone
from .models import *
from .forms import *
from datetime import date, timedelta

# Create your views here.


def index(request):
    return render(request, 'billing/index.html', {})

def search_result(request):
    if request.method == 'POST':
        search_request = request.POST['search_request']
        clients = Client.objects.filter(member_card__icontains=f'{search_request}')
        if clients:
            if len(clients) > 1:
               return HttpResponse('Find more than 2 cards!!!') 
            return redirect('detail_client', id=clients[0].id)
        raise Http404('Нет такой карточки!')

def show_clients(request):
    clients = Client.objects.all()
    return render(request, 'billing/show/clients.html', {
        'clients' : clients,
    })

def show_treners(request):
    treners = Trener.objects.all()
    return render(request, 'billing/show/treners.html', {
        'treners' : treners,
    })

def show_groups(request):
    groups = Group.objects.all()
    return render(request, 'billing/show/groups.html', {
        'groups' : groups,
    })

def show_addresses(request):
    addresses = Address.objects.all()
    return render(request, 'billing/show/addresses.html', {
        'addresses' : addresses,
    })

def show_payments(request):
    payments = Payment.objects.all()
    paginator = Paginator(payments, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'billing/show/payments.html', {
        'payments' : payments,
        'page_obj' : page_obj,
    })

def detail_client(request, id):
    cli = Client.objects.get(id=id)
    groups = cli.groups.all()
    treners = cli.treners.all()
    payments = cli.payment_set.all()
    return render(request, 'billing/detail/client.html', {
        'client': cli,
        'groups': groups,
        'treners': treners,
        'payments': payments,
    })

def detail_group(request, id):
    group = Group.objects.get(id=id)
    group_clients = group.client_set.all()
    return render(request, 'billing/detail/group.html', {
        'group': group,
        'group_clients': group_clients,
    })

def detail_payment(request, id):
    payment = Payment.objects.get(id=id)
    return render(request, 'billing/detail/payment.html', {
        'payment' : payment,
    })

def add_new_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save()
            return redirect('client', id=client.id)
    else:
        form = ClientForm()
    return render(request, 'billing/new_client.html', {
        'form' : form,
    })

def total_payment(payments, date=date.today()):
    result = 0
    for payment in payments:
        if payment.date >= date:
            if payment.payment_to == 'G':
                result += payment.amount
            else:
                result += payment.total_amount()

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
            return redirect('payment', payment.id)
    else:
        form = PaymentForm
    return render(request, 'billing/add_payment.html', {
        'form' : form,
    })