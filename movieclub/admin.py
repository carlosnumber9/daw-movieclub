from django.contrib import admin

# Register your models here.

from movieclub.models import *

admin.site.register(Person)
admin.site.register(Movie)