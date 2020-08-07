from django.db import models

# Create your models here.
class Client(models.Model):
    member_card = models.CharField(max_length=4)
    name = models.CharField(max_length=50)
    tel_number = models.CharField(max_length=20)
    info = models.TextField()
    training_type_choices = [
        ('I', 'Individual'),
        ('G', 'Group'),
        ('B', 'BOTH'),
    ]
    training_type = models.CharField(max_length=1, choices=training_type_choices)

    def __str__(self):
        return self.name

    def client_type(self):
        if self.training_type == 'I':
            self.treners = models.ManyToManyField('Trener')
        elif self.training_type == 'G':
            self.groups = models.ManyToManyField('Group')
        else:
            self.treners = models.ManyToManyField('Trener')
            self.groups = models.ManyToManyField('Group')

    
