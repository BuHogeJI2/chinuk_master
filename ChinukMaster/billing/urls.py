from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search_result, name='search_result'),

    # path('clients', views.show_clients, name='show_clients'),
    # path('treners', views.show_treners, name='show_treners'),
    # path('groups', views.show_groups, name='show_groups'),
    # path('addresses', views.show_addresses, name='show_addresses'),
    # path('payments', views.show_payments, name='show_payments'),

    path('show/<slug:obj>', views.show_objects, name='show_objects'),

    path('<slug:obj>/<int:id>', views.detail_object, name='detail_object'),

    path('new/<slug:obj>', views.add_new_object, name='add_new'),
    path('delete/<int:id>', views.delete_trener, name='delete_trener'),
    path('report', views.get_report, name='get_report'),
]