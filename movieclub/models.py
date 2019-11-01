from django.db import models
import datetime


# Create your models here.

class Person(models.Model):
    name = models.CharField(max_length=100)


class Movie(models.Model):
    name = models.CharField(max_length=100)
    video = models.CharField(max_length=100)
    desc = models.CharField(max_length=1000)
    release = models.DateField(default='', null=True, blank=True)
    director = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='director')
    cast = models.ManyToManyField(Person, related_name='cast')
    poster = models.CharField(max_length=100, null=True, blank=True)
    rating = models.IntegerField(default=5)
    codigo = models.IntegerField(default=0)


'''
(  
    '%Y-%m-%d %H:%M:%S',     # '2006-10-25 14:30:59'  
    '%Y-%m-%d %H:%M:%S.%f',  # '2006-10-25 14:30:59.000200'  
    '%Y-%m-%d %H:%M',        # '2006-10-25 14:30'  
    '%Y-%m-%d',              # '2006-10-25'  
    '%m/%d/%Y %H:%M:%S',     # '10/25/2006 14:30:59'  
    '%m/%d/%Y %H:%M:%S.%f',  # '10/25/2006 14:30:59.000200'  
    '%m/%d/%Y %H:%M',        # '10/25/2006 14:30'  
    '%m/%d/%Y',              # '10/25/2006'  
    '%m/%d/%y %H:%M:%S',     # '10/25/06 14:30:59'  
    '%m/%d/%y %H:%M:%S.%f',  # '10/25/06 14:30:59.000200'  
    '%m/%d/%y %H:%M',        # '10/25/06 14:30'  
    '%m/%d/%y',              # '10/25/06'  
)  
'''






