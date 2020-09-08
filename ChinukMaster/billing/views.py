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
            if payment.payment_to == 'G':
                result += payment.amount
            else:
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

    paginator = Paginator(inst, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    show_obj_link = f'{obj}s' if obj != 'address' else f'{obj}es'

    return render(request, f'billing/show/{show_obj_link}.html', {
        f'{show_obj_link}' : inst,
        'page_obj' : page_obj,
    })

def detail_object(request, obj, id):

    inst = obj_values[obj].objects.get(id=id)
    return render(request, f'billing/detail/{obj}.html', {
        f'{obj}' : inst,
    })

def add_new_object(request, obj):

    form = obj_values[obj]

    if request.method == 'POST':
        form = form(request.POST)
        if form.is_valid():
            obj = form.save()
            return redirect('index')
    else:
        return render(request, 'billing/new_object.html', {
            'obj' : obj,
            'form' : form,
        })

def delete_object(request, obj, id):

    inst = obj_values[obj].objects.get(id=id)
    inst.delete()

    show_obj_link = f'{obj}s' if obj != 'address' else f'{obj}es'

    return redirect('show_objects', show_obj_link)

def get_report(request):
    payments = Payment.objects.all()
    return render(request, 'billing/report.html', {
        'payments': payments,
        'result' : total_payment(payments, date.today()),
    })
