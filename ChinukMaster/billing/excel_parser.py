from pyexcel_xlsx import get_data
from .models import *

group_id = {
    'Иванович пн.ср.пт. 1800' : 9,
    'Иванович вт.чт.сб. 1930' : 10,
    'Пленко пн.ср.пт. 1600' : 11,
    'Мешкуть вт.чт.сб. 1500' : 12,
    'Ермоленко пн.ср.пт. 1930' : 6,
    'Ермоленко вт.чт.сб. 0830' : 13,
    'Шидловская пн.ср.пт. 1930' : 5,
    'Шидловская вт.чт.сб. 1930' : 14,
    'Кобинец пн.ср.пт. 2100' : 15,
    'Романов вт.чт.сб. 1800' : 1,
    'Волк вт.чт.сб. 1700' : 3,
    'Жигар вт.чт.сб. 2100' : 7,

}

def parse_data():

    file_data = get_data('billing/static/Masherova.xlsx')

    for key, value in file_data.items():
        group_name = key
        for person_data in value:
            if len(person_data) < 4:
                for i in range(4 - len(person_data)):
                    person_data.append('')
            parse_client(group_name, person_data[0], person_data[1], person_data[2], person_data[3])



def parse_client(group_name, member_card, name, tel_number, info):
    group = Group.objects.get(id=group_id[group_name])
    
    client = Client.objects.create(member_card=member_card, name=name, tel_number=tel_number, info=info)
    client.save()
    client.groups.add(group)

