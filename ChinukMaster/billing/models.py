from django.db import models
from django.utils import timezone
from datetime import date

# Create your models here.
class Trener(models.Model):
    name = models.CharField(max_length=50, verbose_name = 'Имя')
    tel_number = models.CharField(max_length=20, verbose_name = 'Номер телефона')
    info = models.TextField(blank=True, null=False, verbose_name = 'Дополнительная информация')

    class Meta:
        verbose_name = 'Тренер'
        verbose_name_plural = 'Тренеры'

    def __str__(self):
        return self.name.split(' ')[0]


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

    gr_type = models.CharField(verbose_name='Возраст', max_length=1, choices=gr_type_choices, default='A')
    sport_type = models.CharField(verbose_name='Тип', max_length=1, choices = sport_type_choices, default='T')
    time = models.TimeField(verbose_name='Время')
    trener = models.ForeignKey('Trener', verbose_name='Тренер', on_delete=models.PROTECT, null=True, blank=True)
    address = models.ForeignKey('Address', verbose_name='Зал', on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):

        name = self.trener.name.split()[0]
        return ' '.join([name, str(self.time)])

class Client(models.Model):
    member_card = models.CharField(verbose_name='Членская карта', max_length=4, blank=True, null=True)
    name = models.CharField(verbose_name='ФИО', max_length=50, blank=True, null=True)
    tel_number = models.CharField(verbose_name='Номер телефона', max_length=20, blank=True, null=True)
    info = models.TextField(verbose_name='Дополнительная информация', null=True, blank=True)
    training_type_choices = [
        ('I', 'Индивидуал'),
        ('G', 'В группе'),
        ('B', 'Смешанный'),
    ]
    cl_type = models.CharField(verbose_name='Тип клиента', max_length=1, choices=training_type_choices, default='G')
    treners = models.ManyToManyField(Trener, verbose_name='Тренер', blank=True)
    groups = models.ManyToManyField(Group, verbose_name='Группа', blank=True)

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

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'

    def __str__(self):
        return self.address

class Payment(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name='Плательщик')

    payment_to_choices = [
        ('G', 'В группу'),
        ('I', 'Индивидуально')
    ]
    payment_type_choices = [
        ('O', 'Разовый платеж'),
        ('M', 'Месячный взнос')
    ]

    payment_to = models.CharField(max_length=1, choices=payment_to_choices, default='G', verbose_name='Направление оплаты')
    payment_type = models.CharField(max_length=1, choices=payment_type_choices, default='M', verbose_name='Тип оплаты')
    trener = models.ForeignKey(Trener, on_delete=models.PROTECT, verbose_name='Тренер', blank=True, null=True)
    group = models.ForeignKey(Group, on_delete=models.PROTECT, verbose_name='Группа', blank=True, null=True)
    date = models.DateField(verbose_name='Дата оплаты', default=timezone.now)
    amount = models.FloatField(verbose_name='Сумма', default=60)
    trener_part = models.FloatField(verbose_name='Тренеру', default=0)

    def today(self):
        return date.today()

    def total_amount(self):
        if self.trener_part:
            return self.amount - self.trener_part
        return self.amount

    def __str__(self):
        return f'{self.date}: {self.amount} BYN'

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'