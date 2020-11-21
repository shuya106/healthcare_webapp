from django.db import models

CONDITION = ((0, 'good'), (1, 'normal'), (2, 'bad'))
ACTION = ((0, 'NO'), (1, 'YES'))

class HealthModel(models.Model):

    max_temp = models.FloatField()
    weather = models.CharField(max_length=20)
    condition = models.IntegerField(choices= CONDITION,)
    input_date = models.DateField(unique=True)
    action = models.IntegerField(choices=ACTION,)


    def __str__(self):
        return str(self.input_date)