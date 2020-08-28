from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('client/<int:id>', views.detail_client, name='detail_client'),
    path('group/<int:id>', views.detail_group, name='detail_group'),
    path('client/new', views.add_new_client, name='new_client'),
    path('client/find', views.find_client, name='find_client'),
    path('report', views.get_report, name='get_report'),
]