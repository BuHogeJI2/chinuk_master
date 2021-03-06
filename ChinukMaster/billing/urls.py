from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search_result, name='search_result'),

    path('show/<slug:obj>', views.show_objects, name='show_objects'),
    path('show/payments/<slug:obj>', views.show_payments, name='show_payments'),
    path('<slug:obj>/<int:id>', views.detail_object, name='detail_object'),

    path('edit/<slug:obj>/<int:id>', views.edit_object, name='edit_object'),

    path('delete/<slug:obj>/<int:id>', views.delete_object, name='delete_object'),
    path('delete/duplicated/<slug:obj>/<int:id>', views.delete_duplicated, name='delete_duplicated'),

    path('new/<slug:obj>', views.new_object, name='new_object'),

    path('<slug:obj>/<int:id>/payments/history', views.payments_history, name='payments_history'),

    path('report', views.get_report, name='get_report'),
]