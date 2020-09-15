from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse, Http404
from django.utils import timezone
from .models import *
from .forms import *
from datetime import date, timedelta

# Global varibles

obj_values = {
        'trener' : Trener, 
        'client' : Client,
        'group'  : Group,
        'payment': Payment,
        'address': Address,
    }

obj_forms = {
    'trener' : TrenerForm, 
    'client' : ClientForm,
    'group'  : GroupForm,
    'payment': PaymentForm,
    'address': AddressForm,
}

# Functions-supporters

def get_obj_link(obj):
    for k, v in obj_values.items():
        if v == type(obj):
            obj_link = k
    return obj_link

def total_payment(payments, date=date.today()):
    result = 0
    for payment in payments:
        if payment.date >= date:
            result += payment.total_amount()

    return result

# Views

def index(request):
    return render(request, 'billing/index.html', {})

def search_result(request):

    models = [Client, Trener, Group, Address, Payment]

    if request.method == 'POST':
        search_request = request.POST['search_request']
        query_sets = []

        for model in models:
            if model == Trener or model == Client:
                if search_request.isdigit():
                    if model == Client:
                        objs = model.objects.filter(member_card__contains=f'{search_request}')
                        if objs:
                            query_sets.append(objs)
                    objs = model.objects.filter(tel_number__contains=f'{search_request}')
                    if objs:
                        query_sets.append(objs)
                else:
                    objs = model.objects.filter(name__contains=f'{search_request}')
                    if objs:
                        query_sets.append(objs)

        if query_sets:
            if len(query_sets) == 1:
                objs_set = query_sets[0]
                if len(objs_set) == 1:
                    obj = objs_set[0]
                    obj_link = get_obj_link(obj)
                    return redirect('detail_object', obj=obj_link, id=obj.id)
            obj_pairs = {}
            for query_set in query_sets:
                for obj in query_set:
                    obj_link = get_obj_link(obj)
                    obj_pairs[obj] = obj_link
            return render(request, 'billing/search_result.html', {
                'obj_pairs' : obj_pairs,
            })

            return HttpResponse(query_sets)

        return HttpResponse('Nothing')


def show_objects(request, obj):

    inst = obj_values[obj].objects.all()

    paginator = Paginator(inst, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    show_obj_link = f'{obj}s' if obj != 'address' else f'{obj}es'

    return render(request, f'billing/show/{show_obj_link}.html', {
        f'{show_obj_link}' : inst,
        'page_obj' : page_obj,
    })

def show_payments(request, obj):
    payments = Payment.objects.all()

    payments_group = Payment.objects.filter(payment_to='G')
    payments_individuals = Payment.objects.filter(payment_to='I')

    if obj == 'groups':
        paginator = Paginator(payments_group, 15)
    elif obj == 'individuals':
        paginator = Paginator(payments_individuals, 15)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'billing/show/payments.html', {
        'payment_type' : obj,
        'page_obj' : page_obj, 

    })

def detail_object(request, obj, id):

    inst = obj_values[obj].objects.get(id=id)
    return render(request, f'billing/detail/{obj}.html', {
        f'{obj}' : inst,
    })

def new_object(request, obj):
    form = obj_forms[obj]

    if request.method == 'POST':
        form = form(request.POST)
        if form.is_valid():
            inst = form.save()
            return redirect('detail_object', obj, inst.id)
    else:
        return render(request, 'billing/object_form.html', {
            'obj' : obj,
            'form' : form,
        })

def edit_object(request, obj, id):
    inst = obj_values[obj].objects.get(id=id)

    if request.method == 'POST':
        form = obj_forms[obj](request.POST, instance=inst)
        if form.is_valid():
            inst = form.save()
            return redirect('detail_object', obj, inst.id)
    else:
        form = obj_forms[obj](instance=inst)
        return render(request, 'billing/object_form.html', {
            'obj' : inst,
            'form' : form,
        })

def delete_object(request, obj, id):
    inst = obj_values[obj].objects.get(id=id)
    inst.delete()

    show_obj_link = f'{obj}s' if obj != 'address' else f'{obj}es'

    return redirect('show_objects', obj)

def payments_history(request, obj, id):
    inst = obj_values[obj].objects.get(id=id)

    payments = inst.payment_set.all()

    paginator = Paginator(payments, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'billing/payments_history.html', {
        'inst' : inst,
        'page_obj' : page_obj,
    })

def get_report(request):
    payments = Payment.objects.all()
    return render(request, 'billing/report.html', {
        'payments': payments,
        'total_payment' : total_payment(payments, date.today()),
    })
