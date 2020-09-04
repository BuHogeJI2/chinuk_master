from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search_result, name='search_result'),

    path('clients', views.show_clients, name='show_clients'),
    path('treners', views.show_treners, name='show_treners'),
    path('groups', views.show_groups, name='show_groups'),
    path('addresses', views.show_addresses, name='show_addresses'),
    path('payments', views.show_payments, name='show_payments'),

    path('client/<int:id>', views.detail_client, name='client'),
    path('group/<int:id>', views.detail_group, name='group'),
    path('payment/<int:id>', views.detail_payment, name='payment'),
    path('trener/<int:id>', views.detail_trener, name='trener'),

    path('client/new', views.add_new_client, name='new_client'),
    path('report', views.get_report, name='get_report'),
    path('payment/add', views.add_payment, name='add_payment'),
]