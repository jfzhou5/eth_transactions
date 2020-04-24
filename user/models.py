from django.db import models


# Create your models here.
class Euser(models.Model):
    private_key = models.CharField(max_length=70)
    name = models.CharField(max_length=11)
    password = models.CharField(max_length=45)
    address = models.CharField(max_length=45,default='')

    class Meta:
        db_table = 'Euser'
