from django.db import models

# Create your models here.
class Trener(models.Model):
    name = models.CharField(max_length=50, verbose_name = 'Имя')
    tel_number = models.CharField(max_length=20, verbose_name = 'Номер телефона')
    info = models.TextField(blank=True, null=False, verbose_name = 'Дополнительная информация')

    class Meta:
        verbose_name = 'Тренер'
        verbose_name_plural = 'Тренеры'

    def __str__(self):
        return self.name


class Group(models.Model):

    gr_type_choices = [
        ('A', 'Взрослая'),
        ('C', 'Детская')
    ]

    sport_type_choices = [
        ('B', 'Классический бокс'),
        ('T', 'Тайский бокс'),
        ('W', 'Женская группа'),
        ('M', 'ММА')
    ]

    gr_type = models.CharField(max_length=1, choices=gr_type_choices)
    sport_type = models.CharField(max_length=1, choices = sport_type_choices)
    time = models.TimeField()
    trener = models.ForeignKey('Trener', on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):

        name = self.trener.name.split()[0]
        return ' '.join([name, str(self.time)])

class Client(models.Model):
    member_card = models.CharField(max_length=4, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    tel_number = models.CharField(max_length=20, blank=True, null=True)
    info = models.TextField(null=True, blank=True)
    training_type_choices = [
        ('I', 'Individual'),
        ('G', 'Group'),
        ('B', 'BOTH'),
    ]
    cl_type = models.CharField(max_length=1, choices=training_type_choices, default='G', blank=True, null=True)
    treners = models.ManyToManyField(Trener, blank=True, null=True, related_name='client_trener')
    groups = models.ManyToManyField(Group, blank=True, null=True, related_name='client_group')

    def __str__(self):
        return self.name
            
    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Address(models.Model):

    address_choices = [
        ('Машерова 17/4', 'Машерова 17/4'),
        ('Свердлова 23', 'Свердлова 23')
    ]

    address = models.CharField(max_length=20, choices = address_choices)
    tel_number = models.CharField(max_length = 20)
    groups = models.ForeignKey('Group', on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'

    def __str__(self):
        return self.address