from pyexcel_xlsx import get_data
from .models import *

def parse_data():

    file_data = get_data('billing/static/Masherova.xlsx')

    for key, value in file_data.items():
        list_name = key
        for person_data in value:
            if len(person_data) < 4:
                for i in range(4 - len(person_data)):
                    person_data.append('')
            parse_client(person_data[0], person_data[1], person_data[2], person_data[3])



def parse_client(member_card, name, tel_number, info):
    group_ivanovich = Group.objects.get(id=9)
    client = Client.objects.create(member_card=member_card, name=name, tel_number=tel_number, info=info)
    client.save()
    client.groups.add(group_ivanovich)

