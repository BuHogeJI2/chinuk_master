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
            return redirect('detail_object', obj='client', id=clients[0].id)
        raise Http404('Нет такой карточки!')


def show_objects(request, obj):

    obj_values = {
        'treners' : Trener, 
        'clients' : Client,
        'groups'  : Group,
        'payments': Payment,
        'addresses': Address,
    }

    inst = obj_values[obj].objects.all()

    paginator = Paginator(inst, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, f'billing/show/{obj}.html', {
        f'{obj}' : inst,
        'page_obj' : page_obj,
    })

def detail_object(request, obj, id):

    obj_values = {
        'trener' : Trener, 
        'client' : Client,
        'group'  : Group,
        'payment': Payment,
        'address': Address,
    }

    inst = obj_values[obj].objects.get(id=id)
    return render(request, f'billing/detail/{obj}.html', {
        f'{obj}' : inst,
    })

def add_new_object(request, obj):

    obj_values = {
        'trener' : TrenerForm, 
        'client' : ClientForm,
        'group'  : GroupForm,
        'payment': PaymentForm,
        'address': AddressForm,
    }

    form = obj_values[obj]

    if request.method == 'POST':
        form = form(request.POST)
        if form.is_valid():
            obj = form.save()
            return redirect('index')
    else:
        return render(request, 'billing/add/new_object.html', {
            'obj' : obj,
            'form' : form,
        })

def delete_object(request, obj, id):

    obj_values = {
        'trener' : Trener, 
        'client' : Client,
        'group'  : Group,
        'payment': Payment,
        'address': Address,
    }

    inst = obj_values[obj].objects.get(id=id)
    inst.delete()

    show_obj_link = f'{obj}s' if obj != 'address' else f'{obj}es'

    return redirect('show_objects', show_obj_link)

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